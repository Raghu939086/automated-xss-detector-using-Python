import logging
import csv
from datetime import datetime

def setup_logging(logfile="scan.log"):
    logging.basicConfig(
        filename=logfile,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def print_result(result: dict):
    """
    result example:
    {
        "param": "q",
        "payload": "<script>..",
        "vulnerable": True,
        "similarity": 0.82,
        "notes": "payload found at raw text"
    }
    """
    status = "VULNERABLE" if result["vulnerable"] else "NOT VULNERABLE"
    print(f"[{status}] param={result['param']} payload={result['payload']!r} sim={result['similarity']:.3f}")
    if result.get("notes"):
        print("  Notes:", result["notes"])

def save_csv(results: list, path="report.csv"):
    keys = ["param", "payload", "vulnerable", "similarity", "notes"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        for r in results:
            writer.writerow({k: r.get(k, "") for k in keys})
