"""Minimal ComfyUI API benchmark runner.

Posts an API-format workflow, waits for completion, prints elapsed time.
Usage: bench_run.py <workflow.json> <filename_prefix> [server] [timeout_sec]
"""
import json
import sys
import time
import urllib.request
import urllib.error
import uuid


def http_json(url, payload=None, timeout=10):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    wf_path = sys.argv[1]
    prefix = sys.argv[2]
    server = sys.argv[3] if len(sys.argv) > 3 else "http://127.0.0.1:8188"
    timeout = float(sys.argv[4]) if len(sys.argv) > 4 else 240.0
    seed_override = int(sys.argv[5]) if len(sys.argv) > 5 else None
    w_override = int(sys.argv[6]) if len(sys.argv) > 6 else None
    h_override = int(sys.argv[7]) if len(sys.argv) > 7 else None

    with open(wf_path, "r", encoding="utf-8-sig") as f:
        prompt = json.load(f)

    for node in prompt.values():
        if node.get("class_type") == "SaveImage":
            node["inputs"]["filename_prefix"] = prefix
        if seed_override is not None and node.get("class_type") == "KSampler":
            node["inputs"]["seed"] = seed_override
        if w_override is not None and node.get("class_type") == "EmptyLatentImage":
            node["inputs"]["width"] = w_override
            node["inputs"]["height"] = h_override

    client_id = str(uuid.uuid4())
    t0 = time.time()
    resp = http_json(server + "/prompt", {"prompt": prompt, "client_id": client_id})
    pid = resp["prompt_id"]
    print(f"queued prompt_id={pid}", flush=True)

    while True:
        time.sleep(2)
        elapsed = time.time() - t0
        if elapsed > timeout:
            print(f"TIMEOUT after {elapsed:.1f}s", flush=True)
            sys.exit(2)
        try:
            hist = http_json(server + "/history/" + pid, timeout=10)
        except urllib.error.URLError:
            continue
        if pid not in hist:
            continue
        entry = hist[pid]
        status = entry.get("status", {})
        if status.get("completed"):
            total = time.time() - t0
            print(f"DONE total_wall={total:.1f}s", flush=True)
            print("messages_count:", len(status.get("messages", [])), flush=True)
            sys.exit(0)
        if status.get("status_str") == "error":
            print("ERROR status:", json.dumps(status)[:800], flush=True)
            sys.exit(1)


if __name__ == "__main__":
    main()
