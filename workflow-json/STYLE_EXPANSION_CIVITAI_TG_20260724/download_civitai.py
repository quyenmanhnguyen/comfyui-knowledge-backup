import hashlib
import re
import shutil
import urllib.request
from pathlib import Path

ACC = Path(r"C:\Users\Admin\Documents\ACC.txt")
JOBS = [
    (
        "https://civitai.com/api/download/models/3084665",
        Path(r"C:\AI\ComfyUI\models\loras\AnimaMythP0rtr4itStyleV1.safetensors"),
        "cd9639b03d4458323e696e3792ff7535ae03f9f70368d6d0dc17fe86fa4f354f",
    ),
    (
        "https://civitai.com/api/download/models/3126430",
        Path(r"C:\AI\ComfyUI\models\loras\BunnySlop_v404.safetensors"),
        "6471789277cf26e0cb9589040a13a5d5a03319525b19b76dd42b71fe91722962",
    ),
    (
        "https://civitai.com/api/download/models/2615702",
        Path(r"C:\AI\ComfyUI\models\checkpoints\hassakuXLIllustrious_v34.safetensors"),
        "1618edb443d9c641fb01c4961f5875d5f01b1a851fd9f2ea64623ceac82257e0",
    ),
    (
        "https://civitai.com/api/download/models/2907004",
        Path(r"C:\AI\ComfyUI\models\checkpoints\comix_b3.safetensors"),
        "0df1858f74c367da3c118a747cad1d99b5bf8241c235ec4ca99e91d214bd63ed",
    ),
    (
        "https://civitai.com/api/download/models/3126711",
        Path(r"C:\AI\ComfyUI\models\loras\S1_Dramatic Lighting Anima_V2.safetensors"),
        "d27d2c74bf32222fb3df4515e14a45ab996a59cff3d53e4abfa0f8ed5922399a",
    ),
    (
        "https://civitai.com/api/download/models/2883731",
        Path(r"C:\AI\ComfyUI\models\checkpoints\waiIllustriousSDXL_v170.safetensors"),
        "f116b0c78ff441467b0cdc8f1936e1ed18ea31e9997c7b132b1b8db533f0bd04",
    ),
]


def token():
    if not ACC.exists():
        return None
    text = ACC.read_text(encoding="utf-8-sig", errors="ignore")
    for pattern in (
        r"(?i)citiv(?:ai|ired)[^\r\n:=]{0,30}[:=]\s*([A-Za-z0-9_-]{20,})",
        r"(?i)api[_ -]?key\s*[:=]\s*([A-Za-z0-9_-]{20,})",
    ):
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


def download(url, target, sha256):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        current = hashlib.sha256(target.read_bytes()).hexdigest()
        if current == sha256:
            print(f"verified existing: {target.name}", flush=True)
            return
    partial = target.with_suffix(target.suffix + ".part")
    headers = {"User-Agent": "Mozilla/5.0"}
    secret = token()
    if secret:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}token={secret}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response, partial.open("wb") as out:
        total = int(response.headers.get("Content-Length", 0))
        copied = 0
        while True:
            chunk = response.read(8 * 1024 * 1024)
            if not chunk:
                break
            out.write(chunk)
            copied += len(chunk)
            if total:
                print(f"{target.name}: {copied / total:.1%}", flush=True)
    digest = hashlib.sha256(partial.read_bytes()).hexdigest()
    if digest != sha256:
        raise RuntimeError(f"hash mismatch for {target.name}: {digest}")
    shutil.move(str(partial), str(target))
    print(f"downloaded and verified: {target.name}", flush=True)


for job in JOBS:
    download(*job)
