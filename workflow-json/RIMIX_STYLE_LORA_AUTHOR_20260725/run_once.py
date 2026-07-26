import json
import subprocess
import sys
import time
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(r"C:\AI")
PYTHON = ROOT / r"python_embeded\python.exe"
CONTROL = ROOT / r"workflows\BENCH_CONTROLLED_20260719\bench_matrix.py"
WORKFLOW = (
    Path(sys.argv[1])
    if len(sys.argv) > 1
    else Path(__file__).with_name("RIMIX_STYLE_AUTHOR12_NATIVE.json")
)
SERVER = "http://127.0.0.1:8188"


def api(path, payload=None, timeout=30):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        SERVER + path, data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read())


subprocess.run([str(PYTHON), str(CONTROL), "stop"], check=False)
subprocess.run(
    [str(PYTHON), str(CONTROL), "start", "--mode", "pytorch"], check=True
)
started = time.time()
try:
    graph = json.loads(WORKFLOW.read_text(encoding="utf-8"))
    queued = api("/prompt", {"prompt": graph, "client_id": str(uuid.uuid4())})
    if queued.get("node_errors"):
        raise RuntimeError(json.dumps(queued["node_errors"], ensure_ascii=False))
    prompt_id = queued["prompt_id"]
    while time.time() - started < 480:
        entry = api("/history/" + prompt_id, timeout=10).get(prompt_id)
        if entry and entry.get("status", {}).get("completed"):
            files = [
                image["filename"]
                for output in entry.get("outputs", {}).values()
                for image in output.get("images", [])
            ]
            print(json.dumps({"elapsed_s": round(time.time() - started, 1), "files": files}))
            break
        if entry and entry.get("status", {}).get("status_str") == "error":
            raise RuntimeError(json.dumps(entry["status"], ensure_ascii=False))
        time.sleep(2)
    else:
        raise TimeoutError("480 second cap")
finally:
    subprocess.run([str(PYTHON), str(CONTROL), "stop"], check=False)
