#!/usr/bin/env python3
"""
Setup script for LLM-based poker transcript processing.
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages."""
    print("Installing LLM requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_llm.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def setup_environment():
    """Set up environment variables."""
    print("\nSetting up environment variables...")
    
    # Check for existing API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not openai_key and not anthropic_key:
        print("No API keys found. Please set one of the following:")
        print("\nFor OpenAI:")
        print("  Windows: set OPENAI_API_KEY=your-key-here")
        print("  Linux/Mac: export OPENAI_API_KEY=your-key-here")
        print("\nFor Anthropic:")
        print("  Windows: set ANTHROPIC_API_KEY=your-key-here")
        print("  Linux/Mac: export ANTHROPIC_API_KEY=your-key-here")
        print("\nYou can get API keys from:")
        print("  OpenAI: https://platform.openai.com/api-keys")
        print("  Anthropic: https://console.anthropic.com/")
    else:
        if openai_key:
            print("✅ OPENAI_API_KEY found")
        if anthropic_key:
            print("✅ ANTHROPIC_API_KEY found")

def main():
    """Main setup function."""
    print("Poker LLM Setup")
    print("=" * 20)
    
    # Install requirements
    if not install_requirements():
        return
    
    # Setup environment
    setup_environment()
    
    print("\nSetup complete! You can now run:")
    print("  python create_json.py")
    print("\nTo change LLM provider, edit the LLM_PROVIDER variable in create_json.py")

if __name__ == "__main__":
    main()
