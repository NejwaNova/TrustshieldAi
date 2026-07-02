import sys
import subprocess
import os

def check_and_install_deps():
    print("Checking for Node.js and npm...")
    try:
        # On Windows, we may need shell=True to check commands cleanly
        is_windows = os.name == 'nt'
        subprocess.run(["node", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=is_windows)
        subprocess.run(["npm", "-v"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=is_windows)
        print("Node.js and npm are installed.")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: Node.js and npm are required to run the TrustShield AI backend.")
        print("Please download and install Node.js from https://nodejs.org and try again.")
        sys.exit(1)

    print("Installing Node.js dependencies...")
    try:
        is_windows = os.name == 'nt'
        # Run npm install
        subprocess.run(["npm", "install"], check=True, shell=is_windows)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def run_server():
    print("Starting TrustShield AI Server (Node.js)...")
    # Change working directory to project root if run from elsewhere
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    is_windows = os.name == 'nt'
    try:
        # Run Node server via npm start
        subprocess.run(["npm", "start"], check=True, shell=is_windows)
    except KeyboardInterrupt:
        print("\nStopping TrustShield AI Server...")
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_deps()
    run_server()
