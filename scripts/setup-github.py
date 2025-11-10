#!/usr/bin/env python3
"""
Script to set up and push repository to GitHub
"""

import os
import sys
import subprocess
import requests
import getpass

GITHUB_USER = "groklord"
REPO_NAME = "jenkins_fullstack"
GITHUB_EMAIL = "groklord@yahoo.com"

def get_github_token():
    """Get GitHub token from environment or prompt user"""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("\n" + "="*60)
        print("GitHub Personal Access Token Required")
        print("="*60)
        print("\nGitHub no longer accepts passwords for authentication.")
        print("You need to create a Personal Access Token:\n")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token' -> 'Generate new token (classic)'")
        print("3. Name: 'jenkins_fullstack_push'")
        print("4. Select scope: 'repo' (all)")
        print("5. Click 'Generate token' and copy it\n")
        token = getpass.getpass("Enter your GitHub Personal Access Token: ")
    return token

def create_repo_on_github(token):
    """Create repository on GitHub if it doesn't exist"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Check if repo exists
    url = f'https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"✓ Repository {GITHUB_USER}/{REPO_NAME} already exists")
        return True
    elif response.status_code == 404:
        # Create repository
        print(f"Creating repository {GITHUB_USER}/{REPO_NAME}...")
        url = 'https://api.github.com/user/repos'
        data = {
            'name': REPO_NAME,
            'description': 'Jenkins Fullstack Application with CI/CD',
            'private': False
        }
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            print(f"✓ Repository created successfully")
            return True
        else:
            print(f"✗ Error creating repository: {response.status_code}")
            print(response.json())
            return False
    else:
        print(f"✗ Error checking repository: {response.status_code}")
        print(response.json())
        return False

def configure_git():
    """Configure git user name and email"""
    try:
        subprocess.run(['git', 'config', 'user.name', GITHUB_USER], check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', GITHUB_EMAIL], check=True, capture_output=True)
        print(f"✓ Git configured: {GITHUB_USER} <{GITHUB_EMAIL}>")
    except subprocess.CalledProcessError as e:
        print(f"⚠ Warning: Could not configure git: {e}")

def setup_remote(token):
    """Set up GitHub remote"""
    remote_url = f'https://{token}@github.com/{GITHUB_USER}/{REPO_NAME}.git'
    
    # Check if remote exists
    try:
        result = subprocess.run(['git', 'remote', 'get-url', 'github'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            # Update existing remote
            subprocess.run(['git', 'remote', 'set-url', 'github', remote_url], check=True)
            print("✓ Updated GitHub remote")
        else:
            # Add new remote
            subprocess.run(['git', 'remote', 'add', 'github', remote_url], check=True)
            print("✓ Added GitHub remote")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error setting up remote: {e}")
        return False
    return True

def push_to_github():
    """Push to GitHub"""
    print("\nPushing to GitHub...")
    try:
        result = subprocess.run(['git', 'push', '-u', 'github', 'main'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Successfully pushed to GitHub!")
            print(f"\nRepository URL: https://github.com/{GITHUB_USER}/{REPO_NAME}")
            return True
        else:
            print("✗ Error pushing to GitHub:")
            print(result.stderr)
            return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        return False

def main():
    print("="*60)
    print("GitHub Setup and Push Script")
    print("="*60)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("✗ Error: Not a git repository")
        sys.exit(1)
    
    # Get token
    token = get_github_token()
    if not token:
        print("✗ No token provided")
        sys.exit(1)
    
    # Configure git
    configure_git()
    
    # Create repository on GitHub
    if not create_repo_on_github(token):
        sys.exit(1)
    
    # Set up remote
    if not setup_remote(token):
        sys.exit(1)
    
    # Push to GitHub
    if push_to_github():
        print("\n" + "="*60)
        print("✓ Setup complete!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("✗ Push failed. Please check the errors above.")
        print("="*60)
        sys.exit(1)

if __name__ == '__main__':
    main()

