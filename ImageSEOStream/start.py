#!/usr/bin/env python3
"""
ImgSage - Advanced AI Image Analyzer & SEO Optimizer
Start script for the application
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Main entry point for the application"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Check if app.py exists
    app_path = script_dir / "app.py"
    if not app_path.exists():
        print("❌ Error: app.py not found in the current directory")
        sys.exit(1)
    
    # Get the port from environment variable or use default
    port = os.getenv("PORT", "8501")
    
    # Build the streamlit command
    cmd = [
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    print(f"🚀 Starting ImgSage on port {port}...")
    print(f"📁 Working directory: {script_dir}")
    print(f"🔧 Command: {' '.join(cmd)}")
    
    try:
        # Run the streamlit application
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down ImgSage...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
