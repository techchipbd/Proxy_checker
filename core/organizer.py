import hashlib

def dedupe(proxies):
    seen=set(); out=[]
    for p in proxies:
        h=hashlib.md5(f"{p['type']}{p['server']}{p['port']}".encode()).hexdigest()
        if h in seen: continue
        seen.add(h); out.append(p)
    return out

def rename(proxies):
    for i,p in enumerate(proxies,1):
        if not p.get("name"):
            p["name"]=f"{p['type'].upper()}-{i:03d}"
    return proxies
