#!/usr/bin/env python
"""
Start Django server with proper ASGI support for WebSockets
"""
import os
import sys
import subprocess
import signal
import time

def kill_existing_servers():
    """Kill any existing Python processes on port 8000"""
    try:
        # Kill existing python processes
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                      capture_output=True, text=True)
        time.sleep(2)
    except:
        pass

def install_requirements():
    """Install required packages"""
    try:
        import daphne
        print("✓ Daphne is installed")
    except ImportError:
        print("Installing daphne...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'daphne'])
    
    try:
        import channels
        print("✓ Channels is installed")
    except ImportError:
        print("Installing channels...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'channels'])

def start_server():
    """Start the Django server with ASGI support"""
    os.chdir('e:/Meeting_app/meeting_app')
    
    print("\n" + "="*50)
    print("Starting Django Meeting App Server")
    print("="*50)
    print("🌐 URL: http://localhost:8000")
    print("📹 Camera access should work on localhost")
    print("🎨 Whiteboard will work with WebSocket support")
    print("="*50)
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Start with daphne (ASGI server that supports WebSockets)
        subprocess.run([
            sys.executable, '-m', 'daphne',
            '-b', 'localhost',
            '-p', '8000',
            'meeting_app.asgi:application'
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except FileNotFoundError:
        print("Daphne not found. Trying with manage.py runserver...")
        try:
            subprocess.run([
                sys.executable, 'manage.py', 'runserver', 'localhost:8000'
            ])
        except KeyboardInterrupt:
            print("\n\nServer stopped.")

if __name__ == '__main__':
    kill_existing_servers()
    install_requirements()
    start_server()