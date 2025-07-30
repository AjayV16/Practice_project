"""
Run script for Video Learning Assistant
"""
import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ All packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        print("Try running: pip install -r requirements.txt")
        sys.exit(1)

def check_env_file():
    """Check if .env file exists and has API keys"""
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        print("Please create a .env file with your API keys")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
        
    if "VIDEODB_API_KEY=" in content and len(content.split("VIDEODB_API_KEY=")[1].split("\n")[0].strip()) > 0:
        print("✅ VideoDB API key found")
        has_videodb = True
    else:
        print("⚠️ VideoDB API key not found in .env file")
        has_videodb = False
    
    if "OPENAI_API_KEY=" in content and len(content.split("OPENAI_API_KEY=")[1].split("\n")[0].strip()) > 0:
        print("✅ OpenAI API key found")
    else:
        print("⚠️ OpenAI API key not found (optional)")
    
    return has_videodb

def run_app():
    """Run the Streamlit app"""
    print("🚀 Starting Video Learning Assistant...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "5000"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    print("🎓 Video Learning Assistant Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Install requirements
    install_requirements()
    
    # Check environment file
    if check_env_file():
        print("\n✅ Setup complete! Starting application...")
        run_app()
    else:
        print("\n❌ Setup incomplete")
        print("Please add your VideoDB API key to the .env file")
        print("Get your API key from: https://console.videodb.io")