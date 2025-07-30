import time
import re
from datetime import datetime

log_file = "/usr/local/var/log/suricata/fast.log"

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def parse_alert(line):
    pattern = r"\[\*\*\] \[(\d+:\d+:\d+)\] (.*?) \[\*\*\] \[Classification: (.*?)\] \[Priority: (\d+)\] \{(.*?)\} (\d+\.\d+\.\d+\.\d+):(\d+) -> (\d+\.\d+\.\d+\.\d+):(\d+)"
    match = re.search(pattern, line)
    if match:
        sid = match.group(1)
        signature = match.group(2)
        classification = match.group(3)
        priority = match.group(4)
        protocol = match.group(5)
        src_ip = match.group(6)
        src_port = match.group(7)
        dst_ip = match.group(8)
        dst_port = match.group(9)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] ALERT (SID {sid}) [{classification}] {signature} | Priority: {priority} | {protocol} {src_ip}:{src_port} → {dst_ip}:{dst_port}"
    return None

try:
    with open(log_file, "r") as f:
        for line in follow(f):
            parsed = parse_alert(line)
            if parsed:
                print(parsed)
except FileNotFoundError:
    print(f"Log file not found: {log_file}")
except PermissionError:
    print("Permission denied. Try running with sudo.")

