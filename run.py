import os
import subprocess
import sys
from main import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def build_client():
    print("Building client...")
    client_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client')
    try:
        subprocess.run(['npm', 'install'], cwd=client_dir, check=True)
        subprocess.run(['npm', 'run', 'build'], cwd=client_dir, check=True)
        print("Client built successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error building client: {e}")
        sys.exit(1)

def main():
    # Get port from environment variable or use default
    port = int(os.getenv('PORT', 5000))
    
    # Check if we're in production
    if os.getenv('FLASK_ENV') == 'production':
        # In production, assume client is already built
        print("Starting production server...")
        subprocess.run(['gunicorn', 'main:app', '--bind', f'0.0.0.0:{port}'])
    else:
        # In development, build client and use Flask server
        build_client()
        print("Starting Flask development server...")
        app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    main() 