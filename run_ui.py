"""
Launch script for FAO-Sim Web UI.

Usage:
    python run_ui.py
"""

import subprocess
import sys
from pathlib import Path


def main():
    """Launch Streamlit app."""
    app_path = Path(__file__).parent / "faosim" / "ui" / "app.py"

    if not app_path.exists():
        print(f"❌ Error: App file not found at {app_path}")
        sys.exit(1)

    print("🚀 Starting FAO-Sim Web UI...")
    print(f"📂 App location: {app_path}")
    print("\n" + "="*60)
    print("The app will open in your browser automatically.")
    print("Press Ctrl+C to stop the server.")
    print("="*60 + "\n")

    # Run Streamlit
    subprocess.run([
        "streamlit", "run",
        str(app_path),
        "--server.port=8501",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false"
    ])


if __name__ == "__main__":
    main()
