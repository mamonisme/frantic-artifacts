import json, urllib.request, urllib.error, os

MCP="https://api.gofrantic.com/mcp"
HDR={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
KID=os.environ["AGENT_KID"]
TOK=os.environ["AGENT_TOKEN"]

def rpc(_id, method, params=None, sid=None):
    body=json.dumps({"jsonrpc":"2.0","id":_id,"method":method,"params":params or {}}).encode()
    h=dict(HDR)
    if sid: h["Mcp-Session-Id"]=sid
    req=urllib.request.Request(MCP, data=body, headers=h, method="POST")
    try:
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
    except urllib.error.HTTPError as e:
        return {"error":e.read().decode()[:800]}, sid

sid=None
_, sid = rpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"frantic-loop-probe","version":"1.0"}})
rpc(2,"notifications/initialized",{},sid)

# CLAIM bounty 105
r, sid = rpc(6,"tools/call",{"name":"frantic.claim_bounty","arguments":{"bounty":"105","agent_kid":KID,"agent_token":TOK}},sid)
print("CLAIM RESULT:")
print(json.dumps(r, indent=1)[:1500])
# extract claim_id
res = r.get("result",{})
# MCP returns content blocks; find text
claim_id=None
if isinstance(res, dict):
    sc = res.get("structuredContent") or {}
    # sometimes nested
    print("structuredContent keys:", list(sc.keys()) if isinstance(sc,dict) else sc)
