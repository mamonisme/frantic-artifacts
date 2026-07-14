import json, urllib.request, urllib.error, os
MCP="https://api.gofrantic.com/mcp"
HDR={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
KID=os.environ["AGENT_KID"]; TOK=os.environ["AGENT_TOKEN"]
CLAIM="3214902e-7607-4721-8586-41cea857fa90"
COMMIT="480f80681d371fed37f5d91a6a03a487d5d7c7c8"
def rpc(_id, method, params=None, sid=None):
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
sid=None
_, sid = rpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"frantic-loop-probe","version":"1.0"}})
rpc(2,"notifications/initialized",{},sid)
artifacts=[
  "public_url=https://github.com/mamonisme/frantic-mcp-loop",
  "evidence_json=https://raw.githubusercontent.com/mamonisme/frantic-mcp-loop/%s/evidence.json" % COMMIT,
  "receipt_ref=runx:receipt:c6be382ec94b62a1be589fe0c8d581837f549027b6bce93595c19f79e761ee4c",
  "report=https://raw.githubusercontent.com/mamonisme/frantic-mcp-loop/%s/report.md" % COMMIT
]
r, sid = rpc(7,"tools/call",{"name":"frantic.submit_delivery","arguments":{
  "claim_id":CLAIM,
  "agent_kid":KID,
  "agent_token":TOK,
  "artifact_refs":artifacts
}},sid)
print(json.dumps(r, indent=1)[:2000])
