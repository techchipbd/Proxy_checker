import json

def parse_outbounds_json(text):
    try:
        j=json.loads(text)
        obs=j.get("outbounds",[])
    except:
        return []
    out=[]
    for o in obs:
        if not o.get("server"): continue
        out.append({
            "type":o.get("type"),
            "server":o.get("server"),
            "port":o.get("server_port"),
            "name":o.get("tag"),
            "tls":bool(o.get("tls",{}).get("enabled")),
            "raw":{"json":o}
        })
    return out
