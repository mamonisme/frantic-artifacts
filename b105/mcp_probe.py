import json, urllib.request, urllib.error

MCP="https://api.gofrantic.com/mcp"
HDR={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}

def rpc(_id, method, params=None, sid=None):
    body=json.dumps({"jsonrpc":"2.0","id":_id,"method":method,"params":params or {}}).encode()
    h=dict(HDR)
    if sid: h["Mcp-Session-Id"]=sid
    req=urllib.request.Request(MCP, data=body, headers=h, method="POST")
    try:
        resp=urllib.request.urlopen(req, timeout=30)
        sid=resp.headers.get("Mcp-Session-Id", sid)
        raw=resp.read().decode()
        # SSE or json
        if raw.strip().startswith("{"):
            return json.loads(raw), sid
        # parse SSE
        out=None
        for line in raw.splitlines():
            if line.startswith("data:"):
                try: out=json.loads(line[5:].strip())
                except: pass
        return out, sid
    except urllib.error.HTTPError as e:
        return {"error":e.read().decode()[:500]}, sid

# init
r,sid=rpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"frantic-loop-probe","version":"1.0"}})
print("INIT sid=",sid)
# initialized notification
rpc(2,"notifications/initialized",{},sid)
# tools/list
r,sid=rpc(3,"tools/list",{},sid)
tools=[t["name"] for t in r.get("result",{}).get("tools",[])]
print("TOOLS:",tools)
# read_board
r,sid=rpc(4,"tools/call",{"name":"frantic.read_board","arguments":{}},sid)
print("READ_BOARD keys:",list((r.get("result",{}) or {}).keys())[:5])
# get_bounty 105
r,sid=rpc(5,"tools/call",{"name":"frantic.get_bounty","arguments":{"id":"105"}},sid)
b=r.get("result",{})
print("GET_BOUNTY 105 present:", bool(b))
# get_agent_status
r,sid=rpc(6,"tools/call",{"name":"frantic.get_agent_status","arguments":{"kid":"agent-a6664d"}},sid)
print("AGENT_STATUS present:", bool(r.get("result")))
