#!/usr/bin/env bash
set -euo pipefail
URL="${1:-https://gofrantic.com/v1/board}"
RESP=$(curl -s --max-time 30 "$URL")
python3 - "$RESP" <<'PY' > board_snapshot.json
import sys, json
resp = sys.argv[1]
d = json.loads(resp)
open_b = d.get("board", {}).get("open_bounties", 0)
host = d.get("channel", {}).get("primary", "unknown")
out = {
  "board_snapshot": {"open_bounties": open_b, "live_host": host, "source": "https://gofrantic.com/v1/board"},
  "open_bounties": open_b,
  "live_host": host
}
print(json.dumps(out))
PY
cat board_snapshot.json
