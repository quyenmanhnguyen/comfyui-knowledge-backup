"""ComfyUI MCP server (stdio) for the C:\\AI setup.

Exposes tools to check status, queue API-format workflow JSON files,
wait for completion, and list recent outputs.

Run: C:\\AI\\python_embeded\\python.exe C:\\AI\\mcp\\comfyui_mcp.py
"""
import json
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from mcp.server.fastmcp import FastMCP

SERVER = "http://127.0.0.1:8188"
OUTPUT_DIR = Path(r"C:\AI\ComfyUI\output")
ALLOWED_ROOT = Path(r"C:\AI")

mcp = FastMCP("comfyui")


def _http_json(url, payload=None, timeout=10):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def api_status():
    """Return system stats if the ComfyUI API is reachable."""
    try:
        stats = _http_json(SERVER + "/system_stats", timeout=5)
    except Exception as exc:  # noqa: BLE001
        return {"reachable": False, "error": str(exc)}
    devs = [
        {"name": d.get("name"), "vram_total": d.get("vram_total"), "vram_free": d.get("vram_free")}
        for d in stats.get("devices", [])
    ]
    return {"reachable": True, "comfyui_version": stats.get("system", {}).get("comfyui_version"), "devices": devs}


def queue_workflow_file(workflow_path, filename_prefix=None, seed=None, width=None, height=None):
    """Queue an API-format workflow JSON. Returns prompt_id."""
    path = Path(workflow_path).resolve()
    if ALLOWED_ROOT not in path.parents and path.parent != ALLOWED_ROOT:
        raise ValueError(f"workflow must be inside {ALLOWED_ROOT}")
    if not path.is_file():
        raise FileNotFoundError(str(path))
    with open(path, "r", encoding="utf-8-sig") as f:
        prompt = json.load(f)
    for node in prompt.values():
        ct = node.get("class_type")
        if ct == "SaveImage" and filename_prefix:
            node["inputs"]["filename_prefix"] = filename_prefix
        elif ct == "KSampler" and seed is not None:
            node["inputs"]["seed"] = int(seed)
        elif ct == "EmptyLatentImage" and width is not None and height is not None:
            node["inputs"]["width"] = int(width)
            node["inputs"]["height"] = int(height)
    resp = _http_json(SERVER + "/prompt", {"prompt": prompt, "client_id": str(uuid.uuid4())}, timeout=30)
    return {"prompt_id": resp["prompt_id"], "number": resp.get("number")}


def wait_prompt(prompt_id, timeout_sec=240.0):
    """Wait for a queued prompt to finish. Returns status and elapsed seconds."""
    t0 = time.time()
    while True:
        elapsed = time.time() - t0
        if elapsed > float(timeout_sec):
            return {"state": "timeout", "elapsed_sec": round(elapsed, 1)}
        try:
            hist = _http_json(f"{SERVER}/history/{prompt_id}", timeout=10)
        except urllib.error.URLError:
            time.sleep(2)
            continue
        entry = hist.get(prompt_id)
        if not entry:
            time.sleep(2)
            continue
        status = entry.get("status", {})
        if status.get("completed"):
            images = [
                o.get("images", [])
                for o in entry.get("outputs", {}).values()
                if isinstance(o, dict)
            ]
            flat = [img["filename"] for sub in images for img in sub if "filename" in img]
            return {"state": "completed", "elapsed_sec": round(time.time() - t0, 1), "images": flat}
        if status.get("status_str") == "error":
            return {"state": "error", "elapsed_sec": round(time.time() - t0, 1),
                    "detail": json.dumps(status)[:600]}
        time.sleep(2)


def recent_outputs(count=10):
    """List newest PNG files in the ComfyUI output directory."""
    files = sorted(OUTPUT_DIR.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [{"name": p.name, "bytes": p.stat().st_size} for p in files[: int(count)]]


def queue_remaining():
    """Return number of running and pending prompts."""
    q = _http_json(SERVER + "/queue", timeout=10)
    return {
        "running": len(q.get("queue_running", [])),
        "pending": len(q.get("queue_pending", [])),
    }


@mcp.tool()
def comfy_status():
    """Check whether ComfyUI is running and return GPU/VRAM info."""
    return api_status()


@mcp.tool()
def comfy_queue(workflow_path: str, filename_prefix: str = "", seed: int = -1,
                width: int = -1, height: int = -1):
    """Queue an API-format ComfyUI workflow JSON (from C:\\AI\\workflows).

    CONFIRMATION REQUIRED: this tool consumes GPU and writes output files.
    The caller must obtain explicit user confirmation before invoking it.
    Read-only tools (comfy_status, comfy_wait, comfy_recent_outputs,
    comfy_queue_remaining) may run without confirmation.
    Never write prompt text, tokens, or secret paths into logs.

    Optional overrides: filename_prefix, seed, width/height (use -1 to keep
    workflow values).
    """
    return queue_workflow_file(
        workflow_path,
        filename_prefix=filename_prefix or None,
        seed=None if seed == -1 else seed,
        width=None if width == -1 else width,
        height=None if height == -1 else height,
    )


@mcp.tool()
def comfy_wait(prompt_id: str, timeout_sec: float = 240.0):
    """Wait for a queued prompt and return completion state, elapsed seconds,
    and produced image filenames."""
    return wait_prompt(prompt_id, timeout_sec)


@mcp.tool()
def comfy_recent_outputs(count: int = 10):
    """List the newest generated PNG files in the ComfyUI output folder."""
    return recent_outputs(count)


@mcp.tool()
def comfy_queue_remaining():
    """Show how many prompts are currently running or pending."""
    return queue_remaining()


if __name__ == "__main__":
    mcp.run()
