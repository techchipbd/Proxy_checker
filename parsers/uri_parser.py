import re, base64, json
from urllib.parse import urlparse, parse_qs

RX=re.compile(r'(vmess|vless|trojan|ss|ssr)://[^\s<>"\']+',re.I)

def parse_uri_list(text):
    out=[]
    for m in RX.finditer(text or ""):
        uri=m.group(0)
        try:
            if uri.startswith("vmess://"):
                d=base64.b64decode(uri[8:]+"===").decode(errors="ignore")
                j=json.loads(d)
                out.append({
                    "type":"vmess",
                    "server":j["add"],
                    "port":int(j["port"]),
                    "name":j.get("ps",""),
                    "tls":j.get("tls")=="tls",
                    "raw":{"uri":uri}
                })
            else:
                u=urlparse(uri)
                out.append({
                    "type":u.scheme,
                    "server":u.hostname,
                    "port":u.port,
                    "name":u.fragment,
                    "tls":"tls" in uri,
                    "raw":{"uri":uri}
                })
        except: pass
    return out
