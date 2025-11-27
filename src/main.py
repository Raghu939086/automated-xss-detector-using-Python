import argparse
from src.scanner import XSSScanner
from src.reporter import setup_logging, print_result, save_csv
import logging

def load_payloads(path=None):
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        logging.warning("Payloads file not found, using defaults")
        return None

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Simple XSS scanner")
    parser.add_argument("--url", required=True, help="Target URL with query parameters, e.g. https://a.com/search?q=test")
    parser.add_argument("--payloads", help="path to payloads file (one per line)")
    parser.add_argument("--output", default="report.csv", help="CSV report path")
    args = parser.parse_args()

    payloads = load_payloads(args.payloads)
    scanner = XSSScanner(args.url, payloads)
    results = scanner.scan()

    for r in results:
        print_result(r)
    save_csv(results, args.output)
    logging.info("Scan complete. Results saved to %s", args.output)

if __name__ == "__main__":
    main()
