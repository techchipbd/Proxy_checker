import yaml

def parse_clash_yaml(text):
    try:
        y=yaml.safe_load(text)
        proxies=y.get("proxies",[])
    except:
        return []
    out=[]
    for p in proxies:
        if not isinstance(p,dict): continue
        out.append({
            "type":p.get("type"),
            "server":p.get("server"),
            "port":p.get("port"),
            "name":p.get("name"),
            "tls":bool(p.get("tls")),
            "raw":{"clash":p}
        })
    return out
