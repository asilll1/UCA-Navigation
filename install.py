#!/usr/bin/env python3
"""
UCA Campus Navigation System - Installation Script
This script helps users install and set up the navigation system.
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_files():
    """Check if all required files are present"""
    print("\n📁 Checking project files...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "templates/index.html",
        "Buildings/Academic block.geojson",
        "Buildings/A1 block.geojson",
        "Buildings/A2 block.geojson",
        "Buildings/B1 block.geojson",
        "Buildings/B2 block.geojson",
        "Paths/Academic block_to_A1 block.geojson"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files are present")
    return True

def main():
    """Main installation function"""
    print("🚀 UCA Campus Navigation System - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check files
    if not check_files():
        print("\n❌ Installation failed: Missing required files")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed: Could not install dependencies")
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the application: python main.py")
    print("2. Open your browser to: http://127.0.0.1:5000")
    print("3. Start navigating the campus!")
    
    # Ask if user wants to run the application now
    try:
        response = input("\n🤔 Would you like to start the application now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("\n🚀 Starting UCA Campus Navigation System...")
            subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Installation completed. Run 'python main.py' when ready!")

if __name__ == "__main__":
    main() 