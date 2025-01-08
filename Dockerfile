# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de requisitos primero
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY src/ ./src/
COPY .env .

# Exponer el puerto para la interfaz web
EXPOSE 5000

# Comando por defecto
CMD ["python", "src/web_interface.py"] 