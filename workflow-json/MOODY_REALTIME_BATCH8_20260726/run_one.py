import json
import sys
import time
import uuid
import urllib.request
from pathlib import Path

SERVER = "http://127.0.0.1:8188"


def queue(path):
    prompt = json.loads(Path(path).read_text(encoding="utf-8"))
    req = json.dumps({"prompt": prompt, "client_id": str(uuid.uuid4())}).encode("utf-8")
    r = urllib.request.Request(SERVER + "/prompt", data=req, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))["prompt_id"]


def wait(prompt_id, timeout=300):
    t0 = time.time()
    while time.time() - t0 < timeout:
        with urllib.request.urlopen(SERVER + f"/history/{prompt_id}", timeout=10) as resp:
            hist = json.loads(resp.read().decode("utf-8"))
        item = hist.get(prompt_id)
        if item:
            images = []
            for out in item.get("outputs", {}).values():
                if isinstance(out, dict):
                    images.extend(out.get("images", []))
            status = item.get("status", {})
            return {
                "state": "complete" if status.get("completed") else status.get("status_str", "done"),
                "elapsed": round(time.time() - t0, 1),
                "images": [img.get("filename") for img in images if img.get("filename")],
                "status": status,
            }
        time.sleep(2)
    return {"state": "timeout", "elapsed": round(time.time() - t0, 1), "images": []}


if __name__ == "__main__":
    path = Path(sys.argv[1])
    pid = queue(path)
    res = wait(pid)
    res["workflow"] = str(path)
    res["prefix"] = path.stem
    print(json.dumps(res, ensure_ascii=False))
