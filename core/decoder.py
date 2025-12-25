import base64
import re

def maybe_decode_base64(text: str) -> str:
    t = (text or "").strip()
    if re.search(r'(vmess|vless|trojan|ss|ssr)://', t, re.I):
        return t
    if len(t) < 60:
        return t
    if not re.fullmatch(r'[A-Za-z0-9+/=\s\-_]+', t):
        return t
    try:
        s = t.replace("\n","").replace("\r","").replace(" ","")
        s += "=" * (-len(s) % 4)
        d = base64.urlsafe_b64decode(s).decode(errors="ignore")
        if "://" in d or "proxies:" in d or "outbounds" in d:
            return d
    except:
        pass
    return t
