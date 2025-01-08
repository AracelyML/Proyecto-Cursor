# Commit Message Generator con Integración Jira

Herramienta web que automatiza la generación de mensajes de commit y el registro de tiempo en Jira, diseñada específicamente para el flujo de trabajo de Deacero.

## 🚀 Características

- 🤖 Genera mensajes de commit detallados y estructurados usando IA
- 📊 Analiza cambios en repositorios de Bitbucket
- ✅ Muestra historias asignadas en el sprint actual de Jira
- ⏱️ Permite registrar tiempo en las historias de Jira
- 💬 Agrega comentarios automáticamente a las historias
- 🌐 Interfaz web intuitiva

## 📋 Requisitos Previos

- Docker Desktop instalado y en ejecución
- Credenciales configuradas para:
  - Bitbucket
  - Jira
  - OpenAI

## 🛠️ Configuración

1. **Estructura del Proyecto**
```bash
D:\CURSOR PROYECT\
├── src/
│   ├── web_interface.py
│   ├── commit_analyzer.py
│   ├── bitbucket_integration.py
│   ├── jira_integration.py
│   └── templates/
│       └── index.html
├── Dockerfile
├── requirements.txt
├── README.md
├── .env.example
└── .env  # Este archivo no se comparte
```

2. **Configuración del archivo .env**
   - Copia el archivo `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edita el archivo `.env` con tus credenciales:
     - Bitbucket: Username y App Password
     - OpenAI: API Key
     - Jira: Email y API Token

   > ⚠️ **IMPORTANTE**: Nunca compartas o subas al repositorio tu archivo `.env`

3. **Obtención de Credenciales**
   - **Bitbucket App Password**:
     1. Ve a Bitbucket.org → Tu perfil
     2. Personal Settings → App Passwords
     3. Create app password
     4. Selecciona permisos de lectura de repositorio

   - **OpenAI API Key**:
     1. Ve a platform.openai.com
     2. API keys → Create new secret key

   - **Jira API Token**:
     1. Ve a id.atlassian.net
     2. Security → API tokens
     3. Create API token

## 🐳 Uso con Docker

1. **Construir la imagen**
```bash
docker build -t commit-generator .
```

2. **Ejecutar el contenedor**
```bash
docker run -p 5000:5000 -it commit-generator
```

3. **Acceder a la aplicación**
- Abre tu navegador y ve a `http://localhost:5000`

## 🔄 Flujo de Trabajo

1. La aplicación muestra los últimos cambios del repositorio
2. Genera un mensaje de commit usando IA
3. Puedes aceptar el mensaje generado o escribir uno personalizado
4. Selecciona una historia de Jira y registra el tiempo

## ⚠️ Solución de Problemas

1. **Para detener la aplicación:**
```bash
docker stop commit-generator
```

2. **Para reconstruir después de cambios:**
```bash
docker build -t commit-generator .
docker run -p 5000:5000 -it commit-generator
```

## 🔐 Seguridad

- No compartas tu archivo .env
- Mantén tus tokens seguros
- Rota tus credenciales periódicamente
- Usa los permisos mínimos necesarios en los tokens

## 📞 Soporte

Para soporte contacta a:
- Equipo de Desarrollo
- Administrador de Jira
- Administrador de Bitbucket

## 🔄 Actualizaciones

Para mantener el proyecto actualizado:
1. Pull los últimos cambios
2. Reconstruye la imagen de Docker
3. Verifica las nuevas variables de entorno
    