"""
Installer script to set up wyoming-macos-tts as a background service.
Handles creating a launcher, configuring launchctl, and verifying service status.
"""

import asyncio
import os
import plistlib
import shutil
import subprocess
import sys
from pathlib import Path
from time import sleep

from wyoming.client import AsyncTcpClient
from wyoming.info import Describe

_LAUNCHER_NAME = "WyomingTTS"
_LABEL = "com.openhoster.wyoming-macos-tts"
_REQUIREMENTS = ["uv", "ffmpeg"]
_DIR = Path(__file__).parent
_PROGRAM_DIR = _DIR.parent
_LAUNCHER_PATH = _PROGRAM_DIR / _LAUNCHER_NAME
_PLIST_PATH = Path.home() / f"Library/LaunchAgents/{_LABEL}.plist"
_LAUNCHER_SCRIPT = """
#!/bin/bash
exec uv run -m wyoming_macos_tts \\
    --uri tcp://0.0.0.0:10200 \\
    --service-name macos-tts \\
    --log-dir ./logs \\
    --log-keep-days 7 "$@"
"""


def verify_requirements():
    """Verify requirmenets are installed"""
    for requirement in _REQUIREMENTS:
        if not shutil.which(requirement):
            print(f"Error. {requirement} is not installed")
            sys.exit(1)
    print("Requirements are installed.")


def save_launcher():
    """Save the launcher script."""
    with open(_LAUNCHER_PATH, "w") as file:
        file.write(_LAUNCHER_SCRIPT)
    subprocess.check_call(["chmod", "+x", str(_LAUNCHER_PATH)])
    print(f"Launcher saved at: {_LAUNCHER_PATH}")


def save_plist():
    """Save the plist file."""
    plist = {
        "Label": _LABEL,
        "ProgramArguments": [str(_LAUNCHER_PATH)],
        "RunAtLoad": True,
        "KeepAlive": True,
        "WorkingDirectory": str(_PROGRAM_DIR),
        "EnvironmentVariables": {"PATH": os.environ["PATH"]},
    }
    with open(_PLIST_PATH, "wb") as file:
        plistlib.dump(plist, file)
    print(f"Plist saved at: {_PLIST_PATH}")


async def verify(max_retries=5, delay=1):
    """Try connecting to the service."""
    client = AsyncTcpClient("localhost", 10200)
    for attempt in range(max_retries):
        try:
            await client.connect()
            await client.write_event(Describe().event())
            event = await client.read_event()
            assert event is not None
            print("Service is running")
            return
        except Exception:
            if attempt == max_retries - 1:
                print("Failed to connect to the service")
                sys.exit(1)
            sleep(delay)
        finally:
            try:
                await client.disconnect()
            except Exception:
                pass


def confirm(question):
    """Prompt the user for a yes/no response."""
    return input(f"{question}? (y/n):\n").strip().lower() == "y"


def launchctl(action, check=False):
    """Run a launchctl command for the service plist."""
    subprocess.run(
        ["launchctl", action, str(_PLIST_PATH)], check=check, capture_output=True
    )
    print(f"Service {action}ed")


# --- Main script execution ---
verify_requirements()

if not _LAUNCHER_PATH.exists() or confirm(
    "Launcher exists. Overwrite with default values"
):
    save_launcher()

run_on_login = confirm("Run in the background and on login")

# Stop if running
launchctl("unload")

if run_on_login:
    save_plist()
    launchctl("load", True)
    if confirm("Verify service is running"):
        asyncio.run(verify())
else:
    try:
        os.remove(_PLIST_PATH)
    except Exception:
        pass

print("Done")
