from difflib import SequenceMatcher

def similarity(a: str, b: str) -> float:
    """Return similarity ratio between two strings (0..1)."""
    return SequenceMatcher(None, a, b).ratio()

def is_payload_reflected(response_text: str, payload: str) -> bool:
    """Simple check if payload string appears in response (raw)."""
    return payload in response_text
