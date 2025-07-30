#!/usr/bin/env python3

import os
import subprocess
import time
from datetime import datetime

SURICATA_CMD = [
    "sudo", "suricata",
    "-i", "eth0",
    "-c", "/usr/local/etc/suricata/suricata.yaml",
    "-D"
]
SURICATA_PID_FILE = "/usr/local/var/run/suricata.pid"
ALERT_SCRIPT = "/home/kali/ai-ids-project/alert_to_terminal.py"

def is_suricata_running():
    """Check if Suricata is already running based on PID file."""
    if os.path.exists(SURICATA_PID_FILE):
        try:
            with open(SURICATA_PID_FILE, "r") as f:
                pid = int(f.read().strip())  # ✅ FIXED: added closing )
            result = subprocess.run(["sudo", "kill", "-0", str(pid)],
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL)
            return result.returncode == 0
        except Exception:
            print("⚠️  Stale PID file found. Trying to remove with sudo...")
            subprocess.run(["sudo", "rm", "-f", SURICATA_PID_FILE])
    return False

def start_suricata():
    print("🔹 Starting Suricata...")
    try:
        subprocess.run(SURICATA_CMD, check=True)
        print("✅ Suricata started.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Suricata failed to start: {e}")
        exit(1)

def run_alert_script():
    print("🔹 Running alert processor...")
    try:
        subprocess.run(["sudo", "python3", ALERT_SCRIPT])
    except KeyboardInterrupt:
        print("\n🛑 Script stopped by user.")
    except Exception as e:
        print(f"❌ Failed to run alert processor: {e}")

def main():
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Starting AI-IDS pipeline\n")
    if not is_suricata_running():
        start_suricata()
        time.sleep(2)
    else:
        print("✅ Suricata is already running.")
    run_alert_script()

if __name__ == "__main__":
    main()
