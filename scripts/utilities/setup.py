#!/usr/bin/env python3
"""
Setup script for Instagram Automation Research platform
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        sys.exit(1)

def setup_directories():
    """Create necessary directories"""
    directories = [
        "data/sessions",
        "data/generated_content",
        "data/analytics",
        "logs"
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")

def check_environment():
    """Check environment configuration"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ .env file not found - copying from .env.example")
        try:
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ .env file created from template")
            print("🔧 Please edit .env file with your credentials")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")

def main():
    """Main setup process"""
    print("🚀 Instagram Automation Research - Setup")
    print("=" * 50)

    check_python_version()
    install_requirements()
    setup_directories()
    check_environment()

    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your Instagram credentials")
    print("2. Run tests: python -m pytest tests/")
    print("3. Try examples: python src/examples/content_creators/post_scheduler.py")

if __name__ == "__main__":
    main()