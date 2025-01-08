import os
from openai import OpenAI
from typing import List, Dict
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class FileChange:
    path: str
    status: str  # 'modified', 'added', 'deleted'
    changes: str = ''  # Para archivos modificados

class CommitMessageGenerator:
    def __init__(self):
        load_dotenv()
        # Configurar OpenAI con la API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY no está configurada en el archivo .env")
        
        self.client = OpenAI(api_key=api_key)

    def analyze_changes(self, file_changes: List[FileChange]) -> Dict:
        # Agrupar cambios por tipo
        modified = [f for f in file_changes if f.status == 'modified']
        added = [f for f in file_changes if f.status == 'added']
        deleted = [f for f in file_changes if f.status == 'deleted']
        
        # Generar resúmenes
        changes_summary = self._summarize_modifications(modified)
        new_files = self._format_file_list(added)
        deleted_files = self._format_file_list(deleted)
        
        return {
            'changes_summary': changes_summary,
            'new_files': new_files,
            'deleted_files': deleted_files
        }

    def generate_commit_message(self, changes_dict: Dict) -> str:
        prompt = f"""
        Analiza los siguientes cambios y genera un mensaje de commit detallado:

        RESUMEN DE CAMBIOS:
        {changes_dict['changes_summary']}
        
        ARCHIVOS NUEVOS:
        {changes_dict['new_files']}
        
        ARCHIVOS ELIMINADOS:
        {changes_dict['deleted_files']}
        
        Por favor, genera un mensaje de commit estructurado que incluya:
        1. Un título conciso que resuma el cambio principal (una línea)
        2. Una descripción detallada que incluya:
           - Qué cambios específicos se realizaron
           - Por qué se hicieron estos cambios (si es evidente del contexto)
           - Impacto de los cambios
           - Lista de los archivos principales modificados
        
        El mensaje debe estar en español y ser lo suficientemente detallado para que otros desarrolladores entiendan el alcance completo de los cambios.
        Usa formato de lista cuando sea apropiado para mejorar la legibilidad.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """Eres un experto en generar mensajes de commit detallados y bien estructurados.
                        Tus mensajes siempre incluyen contexto suficiente y explican claramente los cambios realizados.
                        Prefieres ser específico y detallado en lugar de vago o general."""
                    },
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error al generar el mensaje de commit: {str(e)}")
            return "Error al generar el mensaje de commit"

    def _summarize_modifications(self, modified_files: List[FileChange]) -> str:
        if not modified_files:
            return "No files were modified"
        return "\n".join([f"{f.path}: {f.changes}" for f in modified_files])

    def _format_file_list(self, files: List[FileChange]) -> str:
        if not files:
            return "None"
        return "\n".join([f.path for f in files]) 