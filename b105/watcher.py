import json, urllib.request, os, time
MCP="https://api.gofrantic.com/mcp"
HDR={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
KID=os.environ["AGENT_KID"]; TOK=os.environ["AGENT_TOKEN"]
CLAIM="3214902e-7607-4721-8586-41cea857fa90"
COMMIT="b20c9a4fc76d4d64590d9f4cb673c2be7926333c"
def api(path):
    return json.load(urllib.request.urlopen(urllib.request.Request("https://gofrantic.com"+path), timeout=20))
def status_stage():
    d=api("/v1/agents/agent-a6664d/status")
    for it in d.get("work",{}).get("items",[]):
        if it.get("claimId")==CLAIM:
            return it.get("stage"), it.get("status")
    return None,None
def mrpc(_id, method, params=None, sid=None):
    body=json.dumps({"jsonrpc":"2.0","id":_id,"method":method,"params":params or {}}).encode()
    h=dict(HDR)
    if sid: h["Mcp-Session-Id"]=sid
    req=urllib.request.Request(MCP, data=body, headers=h, method="POST")
    resp=urllib.request.urlopen(req, timeout=30)
    sid=resp.headers.get("Mcp-Session-Id", sid)
    raw=resp.read().decode()
    if raw.strip().startswith("{"): return json.loads(raw), sid
    out=None
    for line in raw.splitlines():
        if line.startswith("data:"):
            try: out=json.loads(line[5:].strip())
            except: pass
    return out, sid
print("watching for active+revision_required window...")
for i in range(40):
    st,sts=status_stage()
    print(f"  t{i}: {st} | {sts}")
    if st=="revision_required" and sts=="active":
        print("WINDOW OPEN -> redeliver")
        sid=None
        _, sid=mrp("x",None) if False else (None,None)
        _, sid = mrpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"r","version":"1.0"}})
        mrpc(2,"notifications/initialized",{},sid)
        arts=[
          "public_url=https://github.com/mamonisme/frantic-mcp-loop",
          f"evidence_json=https://raw.githubusercontent.com/mamonisme/frantic-mcp-loop/{COMMIT}/evidence.json",
          "receipt_ref=runx:receipt:c6be382ec94b62a1be589fe0c8d581837f549027b6bce93595c19f79e761ee4c",
          f"report=https://raw.githubusercontent.com/mamonisme/frantic-mcp-loop/{COMMIT}/report.md"
        ]
        r,_=mrpc(7,"tools/call",{"name":"frantic.submit_delivery","arguments":{"claim_id":CLAIM,"agent_kid":KID,"agent_token":TOK,"artifact_refs":arts}},sid)
        txt=r.get("result",{}).get("content",[{}])[0].get("text","")
        print("REDELIVER RESPONSE:", txt[:400])
        break
    time.sleep(8)
