import time
import re
from datetime import datetime

log_file = "/usr/local/var/log/suricata/fast.log"

def follow(file_path):
    with open(file_path, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

def parse_alert(line):
    pattern = r"\[\*\*\] \[(\d+:\d+:\d+)\] (.*?) \[\*\*\] \[Classification: (.*?)\] \[Priority: (\d+)\] \{(.*?)\} (\d+\.\d+\.\d+\.\d+):(\d+) -> (\d+\.\d+\.\d+\.\d+):(\d+)"
    match = re.search(pattern, line)
    if match:
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sid": match.group(1),
            "signature": match.group(2),
            "classification": match.group(3),
            "priority": match.group(4),
            "protocol": match.group(5),
            "src_ip": match.group(6),
            "src_port": match.group(7),
            "dst_ip": match.group(8),
            "dst_port": match.group(9)
        }
    return None
