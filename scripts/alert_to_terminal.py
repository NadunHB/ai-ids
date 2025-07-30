from colorama import init, Fore, Style
import json
import csv
import os
import hashlib
import argparse
from datetime import datetime
from collections import deque
from core_parser import follow, parse_alert, log_file

init(autoreset=True)

# === Parse command-line arguments ===
parser = argparse.ArgumentParser(description="Real-time Suricata alert logger")
parser.add_argument("--min-priority", type=int, default=1, help="Minimum alert priority to log (1=high, 3=low)")
parser.add_argument("--log-dir", default=".", help="Directory to store alert logs")
parser.add_argument("--max-size", type=int, default=1, help="Max file size in MB before rotation")
args = parser.parse_args()

# === Constants ===
MAX_FILE_SIZE = args.max_size * 1024 * 1024
LOG_DIR = args.log_dir
MIN_PRIORITY = args.min_priority

# === File rotation helper ===
def get_rotated_filename(base_name, ext):
    date_str = datetime.now().strftime("%Y-%m-%d")
    index = 0
    while True:
        filename = os.path.join(LOG_DIR, f"{base_name}_{date_str}")
        if index > 0:
            filename += f"_{index}"
        filename += f".{ext}"
        if not os.path.exists(filename) or os.path.getsize(filename) < MAX_FILE_SIZE:
            return filename
        index += 1

# === JSON export ===
def export_alert_to_json(alert_data):
    json_file = get_rotated_filename("alerts", "json")
    try:
        with open(json_file, 'a') as jf:
            json.dump(alert_data, jf)
            jf.write('\n')
    except Exception as e:
        print(f"{Fore.RED}Error writing to JSON: {e}")

# === CSV export ===
def export_alert_to_csv(alert_data):
    csv_file = get_rotated_filename("alerts", "csv")
    fieldnames = [
        'timestamp', 'sid', 'signature', 'classification',
        'priority', 'protocol', 'src_ip', 'src_port', 'dst_ip', 'dst_port'
    ]
    write_header = not os.path.exists(csv_file)
    try:
        with open(csv_file, 'a', newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(alert_data)
    except Exception as e:
        print(f"{Fore.RED}Error writing to CSV: {e}")

# === Deduplication memory ===
recent_alerts = deque(maxlen=50)

# === Main loop ===
try:
    for line in follow(log_file):
        alert = parse_alert(line)
        if alert:
            priority = int(alert['priority'])
            if priority > MIN_PRIORITY:
                continue

            # Deduplication hash
            alert_hash_input = f"{alert['signature']}_{alert['src_ip']}_{alert['dst_ip']}_{priority}"
            alert_hash = hashlib.md5(alert_hash_input.encode()).hexdigest()
            if alert_hash in recent_alerts:
                continue
            recent_alerts.append(alert_hash)

            # Build ordered alert record
            alert_record = {
                "timestamp": alert["timestamp"],
                "sid": alert["sid"],
                "signature": alert["signature"],
                "classification": alert.get("classification", "(null)"),
                "priority": alert["priority"],
                "protocol": alert["protocol"],
                "src_ip": alert["src_ip"],
                "src_port": alert["src_port"],
                "dst_ip": alert["dst_ip"],
                "dst_port": alert["dst_port"]
            }

            # Terminal output
            if priority == 1:
                alert_color = Fore.RED
            elif priority == 2:
                alert_color = Fore.YELLOW
            else:
                alert_color = Fore.CYAN

            print(
                f"{Fore.YELLOW}[{alert['timestamp']}] {alert_color}ALERT! "
                f"{Style.BRIGHT}{alert['signature']}{Style.RESET_ALL} "
                f"{Fore.CYAN}| SID: {alert['sid']} | Priority: {alert['priority']} "
                f"| {alert['protocol']} {alert['src_ip']}:{alert['src_port']} → {alert['dst_ip']}:{alert['dst_port']}"
            )

            export_alert_to_json(alert_record)
            export_alert_to_csv(alert_record)

except FileNotFoundError:
    print(f"{Fore.RED}Log file not found: {log_file}")
except PermissionError:
    print(f"{Fore.RED}Permission denied. Try running with sudo.")
except KeyboardInterrupt:
    print(f"\n{Fore.GREEN}Stopped by user.")
