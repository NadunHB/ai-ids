from core_parser import follow, parse_alert, log_file
import json

output_file = "alerts.json"

try:
    with open(output_file, "a") as out_file:
        for line in follow(log_file):
            alert = parse_alert(line)
            if alert:
                print(f"[JSON] {alert['timestamp']} {alert['signature']}")
                out_file.write(json.dumps(alert) + "\n")
                out_file.flush()
except FileNotFoundError:
    print(f"Log file not found: {log_file}")
except PermissionError:
    print("Permission denied. Try running with sudo.")
