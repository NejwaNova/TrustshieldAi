import sys
import subprocess
import os

def check_and_install_deps():
    print("Checking Python dependencies...")
    try:
        import fastapi
        import uvicorn
        print("Required Python packages (fastapi, uvicorn) are already installed.")
    except ImportError:
        print("Missing dependencies. Installing from requirements.txt...")
        try:
            is_windows = os.name == 'nt'
            # Try to run pip install
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True, shell=is_windows)
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error installing dependencies: {e}")
            sys.exit(1)

def run_server():
    print("Starting TrustShield AI Server (FastAPI)...")
    # Change working directory to project root if run from elsewhere
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    is_windows = os.name == 'nt'
    try:
        # Run backend server via Python
        # Set PYTHONPATH to root directory so backend.server can be imported
        env = os.environ.copy()
        env["PYTHONPATH"] = project_root
        
        # Start server.py
        subprocess.run([sys.executable, "backend/server.py"], check=True, shell=is_windows, env=env)
    except KeyboardInterrupt:
        print("\nStopping TrustShield AI Server...")
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_deps()
    run_server()
