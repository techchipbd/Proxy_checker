def export_uri(proxies):
    return "\n".join(p["raw"]["uri"] for p in proxies if p.get("raw",{}).get("uri"))
