from typing import List, Dict, Tuple
from atlassian import Bitbucket
from commit_analyzer import FileChange
import os
from dotenv import load_dotenv
from datetime import datetime

class BitbucketChangeAnalyzer:
    def __init__(self, username: str, password: str, workspace: str):
        self.bitbucket = Bitbucket(
            url='https://api.bitbucket.org',
            username=username,
            password=password,
            verify_ssl=True
        )
        self.workspace = workspace

    def get_changes(self, repo_slug: str, from_commit: str, to_commit: str) -> Tuple[List[FileChange], str]:
        try:
            endpoint = f'/2.0/repositories/{self.workspace}/{repo_slug}/commits'
            response = self.bitbucket.get(endpoint)
            
            if not response or 'values' not in response:
                raise ValueError("No se pudieron obtener commits")
            
            # Obtener fecha del último commit
            latest_commit = response['values'][0]
            commit_date = latest_commit.get('date', '')
            commit_hash = latest_commit['hash']
            
            # Convertir fecha ISO a formato legible
            if commit_date:
                commit_date = datetime.fromisoformat(commit_date.replace('Z', '+00:00'))
                commit_date = commit_date.strftime("%Y-%m-%d %H:%M:%S")
            
            diff_endpoint = f'/2.0/repositories/{self.workspace}/{repo_slug}/diff/{commit_hash}'
            
            diff = self.bitbucket.get(diff_endpoint)
            if not diff:
                raise ValueError("No se pudo obtener el diff")
            
            changes = []
            for line in diff.splitlines():
                if line.startswith('+++ b/') or line.startswith('--- a/'):
                    file_path = line[6:]
                    changes.append(FileChange(
                        path=file_path,
                        status='modified',
                        changes=line
                    ))
            
            return changes, commit_date
        except Exception as e:
            raise ValueError(f"Error al obtener cambios: {str(e)}") 