import re
import csv

log_path = '/usr/local/var/log/suricata/fast.log'
csv_path = 'suricata_alerts.csv'

pattern = re.compile(r'(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d+)\s+\[\*\*\] \[(\d+):(\d+):(\d+)\] (.*?) \[\*\*\] \[Classification: (.*?)\] \[Priority: (\d+)\] \{(.*?)\} (.*)')

with open(log_path, 'r') as log_file, open(csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([
        'Timestamp', 'GID', 'SID', 'Rev', 'Message',
        'Classification', 'Priority', 'Protocol', 'Traffic'
    ])

    for line in log_file:
        match = pattern.match(line)
        if match:
            writer.writerow(match.groups())

print(f"[+] Done. Parsed alerts written to: {csv_path}")
