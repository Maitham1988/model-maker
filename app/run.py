#!/usr/bin/env python3
"""
One-Click Launcher
Starts the FastAPI server and opens the browser automatically.

Usage:
    python run.py              # Default: localhost:8000
    python run.py --port 3000  # Custom port
    python run.py --no-browser # Don't auto-open browser
"""

import argparse
import sys
import time
import threading
import webbrowser
from pathlib import Path

# Ensure we're running from base/ directory
BASE_DIR = Path(__file__).parent
if BASE_DIR.name != "base":
    print("❌ run.py must be in the base/ directory")
    sys.exit(1)

# Add base/ to sys.path so imports work
sys.path.insert(0, str(BASE_DIR))


def check_dependencies():
    """Check that required packages are installed."""
    missing = []
    for pkg in ["fastapi", "uvicorn", "llama_cpp", "pydantic", "sse_starlette"]:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install -r {BASE_DIR.parent / 'requirements.txt'}")
        sys.exit(1)


def check_config():
    """Check that config.json exists."""
    config_path = BASE_DIR / "config.json"
    if not config_path.exists():
        print("❌ config.json not found.")
        print("   Run tools/install_customer.py first, or copy config_template.json:")
        print(f"   cp {BASE_DIR / 'config_template.json'} {config_path}")
        sys.exit(1)


def open_browser(port: int, delay: float = 1.5):
    """Open the browser after a short delay."""
    time.sleep(delay)
    url = f"http://localhost:{port}"
    print(f"🌐 Opening {url}")
    webbrowser.open(url)


def main():
    parser = argparse.ArgumentParser(description="Launch Local AI Chat")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")
    parser.add_argument(
        "--no-browser", action="store_true", help="Don't open browser"
    )
    args = parser.parse_args()

    print("=" * 50)
    print("  🤖  Local AI Chat — Starting...")
    print("=" * 50)
    print()

    # Pre-flight checks
    check_dependencies()
    check_config()

    # Auto-open browser
    if not args.no_browser:
        t = threading.Thread(target=open_browser, args=(args.port,), daemon=True)
        t.start()

    # Start server
    import uvicorn  # noqa: delayed import after check

    print(f"🚀 Server: http://{args.host}:{args.port}")
    print(f"   Press Ctrl+C to stop\n")

    # Must run from base/ directory for imports to work
    import os
    os.chdir(str(BASE_DIR))

    uvicorn.run(
        "backend.main:app",
        host=args.host,
        port=args.port,
        reload=False,
        log_level="warning",
    )


if __name__ == "__main__":
    main()
