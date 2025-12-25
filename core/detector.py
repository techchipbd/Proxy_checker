def detect_type(text: str) -> str:
    if "proxies:" in text:
        return "clash_yaml"
    if '"outbounds"' in text:
        return "json"
    if "://" in text:
        return "uri"
    return "unknown"
