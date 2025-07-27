# AI-Powered Intrusion Detection System (AI-IDS)

A beginner-friendly, open-source Intrusion Detection System (IDS) that uses machine learning to detect malicious network traffic.

## Features
- Trains on CICIDS2017 public dataset
- Uses RandomForest to classify normal vs. malicious traffic
- Designed for home/lab networks
- Built to grow into a real-time live traffic monitor

## How to Use
1. Download dataset from: https://www.unb.ca/cic/datasets/ids-2017.html
2. Place CSV files in `dataset/` folder
3. Run: `python3 train_model.py`

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Phase 2 (Coming soon!)
Suricata + real-time log capture

Live traffic analysis + alerts

Packaged version for home users
