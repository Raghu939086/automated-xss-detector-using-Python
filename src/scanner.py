import requests
from bs4 import BeautifulSoup
from typing import List
from src.url_utils import parse_url, build_url
from src.compare import similarity, is_payload_reflected
import logging

DEFAULT_PAYLOADS = [
    '"><script>alert(1)</script>',
    '"><img src=x onerror=alert(1)>',
    "<svg/onload=confirm(1)>"
]

class XSSScanner:
    def __init__(self, url: str, payloads: List[str]=None, timeout: int=10):
        self.base, self.params = parse_url(url)
        self.timeout = timeout
        self.payloads = payloads or DEFAULT_PAYLOADS
        logging.info("Scanner initialized for %s with params %s", self.base, self.params.keys())

    def _send(self, url: str):
        try:
            r = requests.get(url, timeout=self.timeout, headers={"User-Agent": "XSSScanner/1.0"})
            return r
        except requests.RequestException as e:
            logging.error("Request error for %s: %s", url, e)
            return None

    def scan(self):
        """
        For every parameter, inject each payload and check responses.
        Return list of result dicts.
        """
        results = []
        # original response (without payload) - help for similarity checks
        original_url = build_url(self.base, {k: v[0] if isinstance(v, list) else v for k, v in self.params.items()})
        orig_resp = self._send(original_url)
        orig_text = orig_resp.text if orig_resp is not None else ""

        for param in list(self.params.keys()):
            # current parameter original value(s)
            orig_value = self.params.get(param, [""])[0]
            for payload in self.payloads:
                # create new params copy and inject payload into current parameter
                new_params = {k: (payload if k == param else (v[0] if isinstance(v, list) else v))
                              for k, v in self.params.items()}
                target_url = build_url(self.base, new_params)
                logging.info("Testing %s with payload on param %s", target_url, param)
                resp = self._send(target_url)
                if resp is None:
                    results.append({
                        "param": param,
                        "payload": payload,
                        "vulnerable": False,
                        "similarity": 0.0,
                        "notes": "no response"
                    })
                    continue

                resp_text = resp.text
                sim = similarity(orig_text, resp_text)
                # basic reflection test
                reflected = is_payload_reflected(resp_text, payload)
                notes = ""
                if reflected:
                    # optionally, inspect where it appears with BeautifulSoup
                    try:
                        soup = BeautifulSoup(resp_text, "lxml")
                        # search text nodes for payload substring
                        if payload in soup.get_text():
                            notes = "payload reflected in page text"
                        else:
                            notes = "payload reflected in raw HTML (maybe attribute)"
                    except Exception:
                        notes = "payload reflected (could not parse DOM)"
                results.append({
                    "param": param,
                    "payload": payload,
                    "vulnerable": bool(reflected),
                    "similarity": sim,
                    "notes": notes
                })
        return results
