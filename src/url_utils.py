from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def parse_url(url: str):
    """
    Return (base_url, params_dict)
    base_url: scheme://netloc/path
    params_dict: {param: [values]}
    """
    parsed = urlparse(url)
    base = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    params = parse_qs(parsed.query)
    return base, params

def build_url(base: str, params: dict):
    """
    Build full URL from base and params (params is dict param->value)
    """
    return base + "?" + urlencode(params, doseq=True)
