import json, urllib.request, os
MCP="https://api.gofrantic.com/mcp"
HDR={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
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
_, sid = rpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"x","version":"1.0"}})
rpc(2,"notifications/initialized",{},sid)
r,sid=rpc(3,"tools/list",{},sid)
for t in r.get("result",{}).get("tools",[]):
    if t["name"] in ("frantic.submit_delivery","frantic.claim_bounty"):
        print("=== %s ==="%t["name"])
        print(json.dumps(t.get("inputSchema",{}), indent=1)[:1500])
