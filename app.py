from flask import render_template
from flask import Flask,request,jsonify,send_file
import asyncio,os,uuid

from core.loader import load_input
from core.decoder import maybe_decode_base64
from core.detector import detect_type
from core.checker import check_tcp,check_tls
from core.organizer import dedupe,rename
from core.geo import enrich

from parsers.uri_parser import parse_uri_list
from parsers.clash_parser import parse_clash_yaml
from parsers.json_parser import parse_outbounds_json

from exporters.uri import export_uri
from exporters.clash_meta import export_clash_meta

app=Flask(__name__)
OUT="outputs"; os.makedirs(OUT,exist_ok=True)

def filter_active(ps,require_tls=False):
    out=[]
    for p in ps:
        s=p["status"]
        if not s.get("tcp"): continue
        if require_tls and p.get("tls") and not s.get("tls"): continue
        out.append(p)
    return out

async def run_checks(ps,mode):
    for p in ps:
        ok,lat=await check_tcp(p["server"],p["port"])
        p["status"]={"tcp":ok,"latency":lat}
        if ok and mode=="tls" and p.get("tls"):
            p["status"]["tls"]=await check_tls(p["server"],p["port"])
    return ps
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/api/process",methods=["POST"])
def api():
    raw=""
    if request.form.get("input_type")=="url":
        raw=load_input(request.form["url"])
    elif request.form.get("input_type")=="file":
        raw=request.files["file"].read().decode(errors="ignore")
    else:
        raw=request.form.get("text","")

    raw=maybe_decode_base64(raw)
    proxies=[]
    proxies+=parse_clash_yaml(raw)
    proxies+=parse_outbounds_json(raw)
    proxies+=parse_uri_list(raw)

    if not proxies:
        return jsonify({"error":"No proxy detected"}),400

    proxies=rename(dedupe(proxies))
    asyncio.run(run_checks(proxies,request.form.get("check_mode","tcp")))
    proxies=[enrich(p) for p in proxies]
    proxies=filter_active(proxies,request.form.get("check_mode")=="tls")

    proxies=sorted(proxies,key=lambda p:p["status"]["latency"] or 999999)

    if not proxies:
        return jsonify({"error":"No active proxy"}),400

    for p in proxies:
        f=p["status"].get("flag","🏳️")
        cc=p["status"].get("country","??")
        p["name"]=f"{f} {cc} | {p['name']}"

    out=export_clash_meta(proxies,request.form.get("clash_mode","rule"))
    fn=f"{OUT}/{uuid.uuid4()}.yaml"
    open(fn,"w",encoding="utf-8").write(out)

    return jsonify({
        "total":len(proxies),
        "download":"/download/"+os.path.basename(fn)
    })

@app.route("/download/<f>")
def dl(f): return send_file(f"{OUT}/{f}",as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)
