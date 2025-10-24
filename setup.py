#!/usr/bin/env python3
"""
Setup script for YouTube Summarizer
This script helps users set up the application quickly.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"OK: Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("OK: Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def setup_env_file():
    """Set up environment file."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("OK: .env file already exists")
        return True
    
    if not env_example.exists():
        print("ERROR: .env.example file not found")
        return False
    
    print("Setting up .env file...")
    print("Please enter your Hugging Face API key:")
    api_key = input("HUGGINGFACE_API_KEY: ").strip()
    
    if not api_key:
        print("ERROR: API key is required")
        return False
    
    # Read example file and replace placeholder
    with open(env_example, 'r') as f:
        content = f.read()
    
    content = content.replace("your_hugging_face_api_key_here", api_key)
    
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("OK: .env file created successfully")
    return True

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    try:
        import config
        import downloader
        import transcriber
        import chunker
        import summarizer
        print("OK: All modules imported successfully")
        return True
    except ImportError as e:
        print(f"ERROR: Import error: {e}")
        return False

def main():
    """Main setup function."""
    print("YouTube Summarizer Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Set up environment file
    if not setup_env_file():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Run the web interface: streamlit run ui.py")
    print("2. Or use CLI: python main.py 'https://youtube.com/watch?v=VIDEO_ID'")
    print("\nFor more information, see README.md")

if __name__ == "__main__":
    main()
