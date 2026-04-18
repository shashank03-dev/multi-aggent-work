import os
from git import Repo
import requests

def push_to_github(local_path: str, repo_name: str, github_token: str):
    """Initializes a local git repo and pushes it to a new GitHub repository."""
    # 1. Create remote repository via API
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"name": repo_name, "private": False}
    
    response = requests.post("https://api.github.com/user/repos", headers=headers, json=data)
    
    if response.status_code == 201:
        repo_json = response.json()
        remote_url = repo_json['clone_url']
        # Add token to URL for auth
        auth_url = remote_url.replace("https://", f"https://{github_token}@")
    elif response.status_code == 422: # Already exists
        user_response = requests.get("https://api.github.com/user", headers=headers)
        username = user_response.json()['login']
        auth_url = f"https://{github_token}@github.com/{username}/{repo_name}.git"
    else:
        return f"Error creating GitHub repo: {response.text}"

    # 2. Local git operations
    try:
        if not os.path.exists(os.path.join(local_path, ".git")):
            repo = Repo.init(local_path)
        else:
            repo = Repo(local_path)
            
        repo.index.add("*")
        repo.index.commit("Initial commit from PDF App Generator")
        
        if 'origin' in repo.remotes:
            origin = repo.remote('origin')
            origin.set_url(auth_url)
        else:
            origin = repo.create_remote('origin', auth_url)
            
        origin.push(refspec='main:main')
        return f"Successfully pushed to {remote_url if 'remote_url' in locals() else auth_url}"
    except Exception as e:
        return f"Error pushing to GitHub: {e}"
