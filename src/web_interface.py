from flask import Flask, render_template, request, jsonify
from commit_analyzer import CommitMessageGenerator
from bitbucket_integration import BitbucketChangeAnalyzer
from jira_integration import JiraTimeLogger
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Inicializar componentes
load_dotenv()
username = os.getenv('BITBUCKET_USERNAME')
password = os.getenv('BITBUCKET_PASSWORD')
workspace = os.getenv('BITBUCKET_WORKSPACE')

bitbucket_analyzer = BitbucketChangeAnalyzer(username, password, workspace)
commit_generator = CommitMessageGenerator()
jira_logger = JiraTimeLogger()

@app.route('/')
def index():
    # Obtener historias de Jira
    issues = jira_logger.get_assigned_issues()
    
    # Obtener y generar mensaje de commit
    changes, last_commit_date = bitbucket_analyzer.get_changes(
        repo_slug='modelo-econometrico',
        from_commit='master',
        to_commit='HEAD'
    )
    changes_dict = commit_generator.analyze_changes(changes)
    commit_message = commit_generator.generate_commit_message(changes_dict)
    
    return render_template('index.html', 
                         issues=issues, 
                         commit_message=commit_message,
                         last_commit_date=last_commit_date)

@app.route('/log_time', methods=['POST'])
def log_time():
    data = request.json
    ticket_id = data.get('ticket_id')
    time_spent = data.get('time_spent')
    commit_message = data.get('commit_message')
    
    try:
        # Agregar comentario
        jira_logger.add_comment(ticket_id, commit_message)
        
        # Registrar tiempo
        jira_logger.log_time(
            ticket_id=ticket_id,
            time_spent=time_spent,
            comment=commit_message
        )
        
        return jsonify({'success': True, 'message': 'Tiempo registrado correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 