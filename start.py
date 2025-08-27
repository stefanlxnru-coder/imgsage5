#!/usr/bin/env python3
"""
🎯 ImgSage - Simple Startup Script
Quick launcher for local development
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the ImgSage application"""
    print("🎯 ImgSage - Magic Image SEO Tool")
    print("=" * 50)
    
    # Check if we're in the right directory
    app_path = Path("ImageSEOStream/app.py")
    if not app_path.exists():
        print("❌ Error: ImageSEOStream/app.py not found!")
        print("Please run this script from the project root directory")
        return 1
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  Warning: OPENAI_API_KEY environment variable not set")
        print("You can set it with: export OPENAI_API_KEY='your-key-here'")
        print("Or enter it in the app interface")
    
    print("🚀 Starting ImgSage...")
    print("📱 The app will open in your default browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⏳ Please wait while the application loads...")
    
    try:
        # Start Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
