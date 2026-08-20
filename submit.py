import json, urllib.request, urllib.error

BOARD = "https://aidc.nadir.sh/model"

TEAM = "10"
BY = "Nadia Al-Mahyawi"
MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"
IMAGE = "ghcr.io/nadiax94/aidc-10-warmup:latest"

def request(url, body=None):
    data = json.dumps(body).encode() if body else None
    headers = {"User-Agent": "aidc-student/1.0"}
    if body:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

status, result = request("http://localhost:8000/generate")

print("my server said", status, result)

if status != 200:
    raise SystemExit("/generate failed")

status, reply = request(BOARD, {
    "team": TEAM,
    "by": BY,
    "model": MODEL,
    "image": IMAGE,
    "tokens_per_sec": result["tokens_per_sec"],
    "sample": result["sample"]
})

print("the board said", status)
print(json.dumps(reply, indent=2))