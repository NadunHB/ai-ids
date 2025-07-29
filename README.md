# 🛡️ AI-IDS – AI-Powered Intrusion Detection System

A real-time, modular Intrusion Detection System (IDS) that integrates with Suricata to monitor, parse, deduplicate, and export network alerts. Designed as the foundation of a scalable SaaS security monitoring product.

---

## 🚀 Features

- ✅ **Real-Time Alert Monitoring** from Suricata `fast.log`
- ⚙️ **Alert Filtering** by priority (1–3)
- 🔁 **Deduplication** using smart hashing of alert fields
- 📦 **Export to CSV & JSON**, with:
  - Rotating file logs (daily and size-based)
- 💻 **Color-coded Terminal Output** for quick triage
- 🧩 **Modular Architecture** for easy upgrades
- 🧪 **Python Virtual Environment** included
- 🛠️ **1-Command Installer** for seamless setup
- 📂 **Clean Project Structure**, GitHub-ready

---

## 📁 Folder Structure

ai-ids-project/
│
├── alert_to_terminal.py # Main real-time alert pipeline
├── core_parser.py # Suricata log tailer and parser
├── export_to_csv.py # CSV exporter
├── export_to_json.py # JSON exporter
├── parse_fastlog_to_csv.py # Offline converter for fast.log files
├── suricata_parser.py # Alert parsing utilities
├── install_and_run.py # Installer script (auto starts Suricata + script)
│
├── alerts_*.csv / *.json # Sample rotated logs
├── parsed_fast_alerts.log # Example log output
├── suricata_alerts.csv # Offline parsed Suricata file
├── venv-suricata/ # Python virtual environment
├── pycache/ # Python bytecode cache
└── README.md # This file

---

## 🖥️ Live Demo (Terminal Preview)

[2025-07-28 22:46:51] ALERT! ET INFO Possible Kali Linux hostname in DHCP Request Packet
| SID: 1:2022973:1 | Priority: 1 | UDP 10.41.128.85:68 → 10.41.128.99:67


---

## 🛠️ Setup & Usage

### 1️⃣ Clone & Install

```bash
git clone https://github.com/NadunHB/ai-ids.git
cd ai-ids/ai-ids-project

2. Run the installer

chmod +x install_and_run.py
./install_and_run.py

This will:

Auto-start Suricata if not already running

Launch the alert parser with logging and filters

⚙️ CLI Options

Flag    	Default	Description
--min-priority	1	Minimum alert priority to process (1–3)
--log-dir	.	Directory to store log files
--max-size	1	Max log file size (MB) before rotation

Example:


sudo python alert_to_terminal.py --min-priority 2 --log-dir /home/kali/ai-ids-logs

📊 Sample Alert Export (CSV)

timestamp	sid	signature	classification	priority	protocol	src_ip	src_port	dst_ip	dst_port

2025-07-28 22:15:41	1:2100366:8	GPL ICMP PING *NIX	Misc activity	3	ICMP	10.41.128.85	8	217.160.0.187	0
2025-07-28 22:15:41	1:9990002:1	[TEST] ANY ICMP Echo Request Detected	(null)	3	ICMP	10.41.128.85	8	217.160.0.187	0

👷‍♂️ Developer Notes
Python 3.10+ recommended

Tail-based log streaming from Suricata

Uses colorama, csv, json, argparse, hashlib, and deque

🧠 Future Goals

Goal	                         Status

🔐 AI anomaly model             🔜 Coming Soon

🌐 Web dashboard (Flask)	🔜 Planned

📦 .deb / .pkg installer	🔜 Planned

☁️ SaaS multi-user support	🔜 Phase 4

📜 License
This project is licensed under the MIT License.

💡 Credits
Created by Nadun Udara – Network Security Specialist & SaaS Developer
Powered by Suricata + Python

⭐ Support the Project
If you like this project, give it a ⭐ on GitHub to support development and help others discover it.


---

Let me know if you want:
- A `.md` file version to download
- A badge set (stars, Python, Suricata, etc.)
- Additional contributors or roadmap sections

Ready to commit this to your repo?






Ask ChatGPT
