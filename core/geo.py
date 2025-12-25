import socket, os
try:
    import geoip2.database
except:
    geoip2=None

MMDB="data/GeoLite2-Country.mmdb"

def flag(cc):
    if not cc or len(cc)!=2: return "🏳️"
    return "".join(chr(127397+ord(c)) for c in cc.upper())

def enrich(proxy):
    try:
        ip=socket.gethostbyname(proxy["server"])
    except:
        ip=None
    cc=None
    if ip and geoip2 and os.path.exists(MMDB):
        try:
            with geoip2.database.Reader(MMDB) as r:
                cc=r.country(ip).country.iso_code
        except:
            pass
    proxy.setdefault("status",{})
    proxy["status"]["ip"]=ip
    proxy["status"]["country"]=cc
    proxy["status"]["flag"]=flag(cc)
    return proxy
