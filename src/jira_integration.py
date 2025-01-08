from jira import JIRA
from typing import Dict, Optional, List
from dotenv import load_dotenv
import os
import re
from datetime import datetime

class JiraTimeLogger:
    def __init__(self):
        load_dotenv()
        self.jira = JIRA(
            server=os.getenv('JIRA_SERVER'),
            basic_auth=(
                os.getenv('JIRA_EMAIL'),
                os.getenv('JIRA_API_TOKEN')
            )
        )
        
    def extract_jira_ticket(self, commit_message: str) -> Optional[str]:
        """Extrae el ID del ticket de Jira del mensaje de commit"""
        # Busca patrones como "ABC-123" en el mensaje
        match = re.search(r'[A-Z]+-\d+', commit_message)
        return match.group(0) if match else None
    
    def log_time(self, ticket_id: str, time_spent: str, comment: str):
        """Registra el tiempo en el ticket de Jira
        
        Args:
            ticket_id: ID del ticket (ej: "ABC-123")
            time_spent: Tiempo en formato Jira (ej: "1h 30m")
            comment: Descripción del trabajo realizado
        """
        try:
            self.jira.add_worklog(
                issue=ticket_id,
                timeSpent=time_spent,
                comment=comment
            )
            print(f"✓ Tiempo registrado en {ticket_id}: {time_spent}")
        except Exception as e:
            print(f"Error al registrar tiempo en Jira: {str(e)}") 
    
    def get_assigned_issues(self) -> List[Dict]:
        """Obtiene las historias asignadas al usuario actual en el sprint activo"""
        try:
            # JQL para buscar historias asignadas al usuario en el sprint actual
            jql = (
                "assignee = currentUser() AND "
                "sprint in openSprints() AND "
                "status != Done "
                "ORDER BY priority DESC"
            )
            
            issues = self.jira.search_issues(jql)
            
            # Formatear la información de cada historia
            formatted_issues = []
            for issue in issues:
                formatted_issues.append({
                    'key': issue.key,
                    'summary': issue.fields.summary,
                    'status': issue.fields.status.name,
                    'priority': issue.fields.priority.name if issue.fields.priority else 'No priority',
                    'time_spent': self._get_time_spent(issue.key),
                    'time_estimate': self._get_time_estimate(issue.key)
                })
            
            return formatted_issues
            
        except Exception as e:
            print(f"Error al obtener historias de Jira: {str(e)}")
            return []
    
    def _get_time_spent(self, issue_key: str) -> str:
        """Obtiene el tiempo total registrado en una historia"""
        issue = self.jira.issue(issue_key)
        seconds = issue.fields.timespent or 0
        return self._format_time(seconds)
    
    def _get_time_estimate(self, issue_key: str) -> str:
        """Obtiene el tiempo estimado restante de una historia"""
        issue = self.jira.issue(issue_key)
        seconds = issue.fields.timeestimate or 0
        return self._format_time(seconds)
    
    def _format_time(self, seconds: int) -> str:
        """Convierte segundos a formato legible (ej: 2h 30m)"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if hours and minutes:
            return f"{hours}h {minutes}m"
        elif hours:
            return f"{hours}h"
        elif minutes:
            return f"{minutes}m"
        return "0m" 
    
    def add_comment(self, ticket_id: str, comment: str):
        """Agrega un comentario a un ticket de Jira
        
        Args:
            ticket_id: ID del ticket (ej: "ABC-123")
            comment: Comentario a agregar
        """
        try:
            self.jira.add_comment(ticket_id, comment)
            print(f"✓ Comentario agregado al ticket {ticket_id}")
        except Exception as e:
            print(f"Error al agregar comentario en Jira: {str(e)}") 