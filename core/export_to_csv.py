from core_parser import follow, parse_alert, log_file
import csv
import os

csv_file = "alerts.csv"
csv_headers = ["timestamp", "sid", "signature", "classification", "priority", "protocol", "src_ip", "src_port", "dst_ip", "dst_port"]

# Write headers only if the file doesn't exist
write_headers = not os.path.exists(csv_file)

try:
    with open(csv_file, "a", newline="") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=csv_headers)
        if write_headers:
            writer.writeheader()

        for line in follow(log_file):
            alert = parse_alert(line)
            if alert:
                print(f"[CSV] {alert['timestamp']} {alert['signature']}")
                writer.writerow(alert)
                out_file.flush()

except FileNotFoundError:
    print(f"Log file not found: {log_file}")
except PermissionError:
    print("Permission denied. Try running with sudo.")
