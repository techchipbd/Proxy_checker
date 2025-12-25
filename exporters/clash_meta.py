import yaml

def export_clash_meta(proxies, mode="rule"):
    cfg={
        "mixed-port":7890,
        "mode":mode,
        "proxies":[],
        "proxy-groups":[{"name":"MAIN","type":"select","proxies":[]}],
        "rules":["MATCH,MAIN"]
    }
    for p in proxies:
        raw=p.get("raw",{}).get("clash")
        if not raw: continue
        name=p["name"]
        e=dict(raw); e["name"]=name
        cfg["proxies"].append(e)
        cfg["proxy-groups"][0]["proxies"].append(name)
    return yaml.dump(cfg,allow_unicode=True,sort_keys=False)
