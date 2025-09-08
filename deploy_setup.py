#!/usr/bin/env python3
"""
Deployment setup script for Django Meeting App
This script helps prepare your app for deployment
"""

import os
import secrets
import subprocess
import sys
from pathlib import Path

def generate_secret_key():
    """Generate a secure secret key for Django"""
    return secrets.token_urlsafe(50)

def create_env_file():
    """Create .env file with secure defaults"""
    env_content = f"""# Production Environment Variables
SECRET_KEY={generate_secret_key()}
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
DJANGO_SETTINGS_MODULE=meeting_app.settings_production
"""
    
    with open('meeting_app/.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with secure secret key")

def setup_git():
    """Initialize git repository if not exists"""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit for deployment'], check=True)
            print("✅ Git repository initialized")
        else:
            print("✅ Git repository already exists")
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git not found. Please install Git first.")
        return False
    
    return True

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Environment variables
.env
.venv
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Deployment
staticfiles/
*.pem
*.key
*.crt
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore file")

def install_production_requirements():
    """Install production requirements"""
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("✅ Production requirements installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False
    return True

def collect_static():
    """Collect static files"""
    try:
        os.chdir('meeting_app')
        subprocess.run([sys.executable, 'manage_production.py', 'collectstatic', '--noinput'], check=True)
        print("✅ Static files collected")
        os.chdir('..')
    except subprocess.CalledProcessError:
        print("❌ Failed to collect static files")
        return False
    return True

def show_deployment_options():
    """Show available deployment options"""
    print("\n" + "="*60)
    print("🚀 DEPLOYMENT OPTIONS")
    print("="*60)
    
    options = [
        ("Railway", "DEPLOY_RAILWAY.md", "Easy, $5/month free credit, WebSocket support"),
        ("Render", "DEPLOY_RENDER.md", "Free tier, good for testing"),
        ("PythonAnywhere", "DEPLOY_PYTHONANYWHERE.md", "Completely free, no WebSocket"),
        ("DigitalOcean", "DEPLOY_DIGITALOCEAN.md", "$200 free credit, full features"),
        ("Heroku", "DEPLOY_HEROKU.md", "Reliable, paid only")
    ]
    
    for i, (name, file, description) in enumerate(options, 1):
        print(f"{i}. {name}")
        print(f"   📄 Guide: {file}")
        print(f"   📝 {description}")
        print()
    
    print("💡 Recommendation: Start with Railway for full features or PythonAnywhere for free hosting")

def main():
    """Main deployment setup function"""
    print("🔧 Django Meeting App - Deployment Setup")
    print("="*50)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Setup steps
    steps = [
        ("Creating environment file", create_env_file),
        ("Creating .gitignore", create_gitignore),
        ("Setting up Git", setup_git),
        ("Installing requirements", install_production_requirements),
        ("Collecting static files", collect_static),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if not step_func():
            print(f"❌ Failed: {step_name}")
            sys.exit(1)
    
    print("\n✅ Deployment setup complete!")
    show_deployment_options()
    
    print("\n🔗 Next Steps:")
    print("1. Choose a deployment platform from the options above")
    print("2. Follow the specific deployment guide")
    print("3. Update ALLOWED_HOSTS in your .env file with your domain")
    print("4. Test your deployed application")

if __name__ == "__main__":
    main()