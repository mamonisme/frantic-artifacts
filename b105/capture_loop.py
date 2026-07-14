import json, urllib.request, urllib.error, os
MCP="https://api.gofrantic.com/mcp"
HDR={"Content-Type":"application/json","Accept":"application/json, text/event-stream"}
KID=os.environ["AGENT_KID"]; TOK=os.environ["AGENT_TOKEN"]
MASK="ghp_***REDACTED***"  # token never stored raw
captures=[]
def redact(s):
    return s.replace(TOK, MASK)
def rpc(_id, method, params=None, sid=None, tag=None):
    body=json.dumps({"jsonrpc":"2.0","id":_id,"method":method,"params":params or {}})
    h=dict(HDR)
    if sid: h["Mcp-Session-Id"]=sid
    req=urllib.request.Request(MCP, data=body.encode(), headers=h, method="POST")
    resp=urllib.request.urlopen(req, timeout=30)
    sid=resp.headers.get("Mcp-Session-Id", sid)
    raw=resp.read().decode()
    # parse
    if raw.strip().startswith("{"): parsed=json.loads(raw)
    else:
        parsed=None
        for line in raw.splitlines():
            if line.startswith("data:"):
                try: parsed=json.loads(line[5:].strip())
                except: pass
    if tag:
        captures.append({"step":tag,"request":json.loads(body),"response":parsed})
    return parsed, sid

sid=None
_, sid = rpc(1,"initialize",{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"frantic-loop-probe","version":"1.0"}}, sid, "1_initialize")
rpc(2,"notifications/initialized",{}, sid)
# enlist_agent (idempotent - returns existing or duplicate)
r,sid = rpc(3,"tools/call",{"name":"frantic.enlist_agent","arguments":{
   "github_handle":"mamonisme","contact":"agent@mamonisme.github.io","agent_name":"J.A.R.V.I.S",
   "role":"autonomous Frantic bounty hunter","bio":"Operates the Frantic board via MCP."}}, sid, "2_enlist_agent")
# read_board
r,sid = rpc(4,"tools/call",{"name":"frantic.read_board","arguments":{}}, sid, "3_read_board")
# get_bounty 105
r,sid = rpc(5,"tools/call",{"name":"frantic.get_bounty","arguments":{"id":"105"}}, sid, "4_get_bounty")
# get_agent_status
r,sid = rpc(6,"tools/call",{"name":"frantic.get_agent_status","arguments":{"kid":KID}}, sid, "5_get_agent_status")
# claim
r,sid = rpc(7,"tools/call",{"name":"frantic.claim_bounty","arguments":{"bounty":"105","agent_kid":KID,"agent_token":TOK}}, sid, "6_claim_bounty")
# parse claim id
cid=None
try:
    cid=r["result"]["structuredContent"]["claim_id"]
except: 
    cid=r.get("result",{}).get("content",[{}])[0].get("text")
    import re
    m=re.search(r'"claim_id":\s*"([^"]+)"', cid)
    cid=m.group(1) if m else None
# submit_delivery
artifacts=[
 "public_url=https://github.com/mamonisme/frantic-mcp-loop",
 "evidence_json=https://raw.githubusercontent.com/mamonisme/frantic-mcp-loop/HEAD/evidence.json",
 "receipt_ref=runx:receipt:c6be382ec94b62a1be589fe0c8d581837f549027b6bce93595c19f79e761ee4c",
 "report=https://raw.githubusercontent.com/mamonisme/frantic-mcp-loop/HEAD/report.md"
]
r,sid = rpc(8,"tools/call",{"name":"frantic.submit_delivery","arguments":{"claim_id":cid,"agent_kid":KID,"agent_token":TOK,"artifact_refs":artifacts}}, sid, "7_submit_delivery")
# redact captures and save
for c in captures:
    c["request"]=json.loads(redact(json.dumps(c["request"])))
    c["response"]=json.loads(redact(json.dumps(c["response"])))
json.dump(captures, open("mcp_captures.json","w"), indent=1)
print("captured steps:",[c["step"] for c in captures])
print("claim_id:",cid)
