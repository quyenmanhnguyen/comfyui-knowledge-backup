import asyncio
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


ROOT = Path(os.environ.get("TELEGRAM_CLIENT_DIR", r"C:\AI\telegram_client"))
TOKEN_FILE = Path(os.environ.get("TELEGRAM_TOKEN_FILE", r"REPLACE_WITH_LOCAL_TOKEN_FILE.txt"))
SESSION = Path(os.environ.get("TELEGRAM_SESSION", str(ROOT / "comfyui_readonly")))
OUT = ROOT / "comfyui_realtime_scan.json"

KEYWORDS = [
    "comfy", "comfyui", "stable diffusion", "sdxl", "z-image", "z image",
    "flux", "anima", "illustrious", "pony", "civitai", "workflow",
    "lora", "checkpoint", "diffusion", "ai绘画", "工作流", "模型",
]


def parse_credentials(text: str):
    api_id = None
    api_hash = None
    phone = None
    for line in text.splitlines():
        raw = line.strip()
        low = raw.lower()
        if not raw or raw.startswith("#"):
            continue
        if "api" in low and "id" in low:
            m = re.search(r"(\d{5,})", raw)
            if m:
                api_id = int(m.group(1))
        if "hash" in low:
            m = re.search(r"([a-fA-F0-9]{32})", raw)
            if m:
                api_hash = m.group(1)
        if "phone" in low or "sdt" in low or "số" in low:
            m = re.search(r"(\+?\d[\d\s-]{7,}\d)", raw)
            if m:
                phone = re.sub(r"[\s-]+", "", m.group(1))
    if api_id is None:
        m = re.search(r"\b(\d{5,})\b", text)
        if m:
            api_id = int(m.group(1))
    if api_hash is None:
        m = re.search(r"\b([a-fA-F0-9]{32})\b", text)
        if m:
            api_hash = m.group(1)
    if phone is None:
        m = re.search(r"(\+\d[\d\s-]{7,}\d)", text)
        if m:
            phone = re.sub(r"[\s-]+", "", m.group(1))
    if not api_id or not api_hash or not phone:
        missing = [k for k, v in {"api_id": api_id, "api_hash": api_hash, "phone": phone}.items() if not v]
        raise RuntimeError("Missing Telegram credential fields: " + ", ".join(missing))
    return api_id, api_hash, phone


def reaction_count(message):
    total = 0
    reactions = getattr(message, "reactions", None)
    if reactions and getattr(reactions, "results", None):
        for item in reactions.results:
            total += int(getattr(item, "count", 0) or 0)
    return total


def compact_text(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:500]


def score_message(message, title):
    text = (message.message or "")
    low = (title + " " + text).lower()
    hits = [k for k in KEYWORDS if k in low]
    media_bonus = 2 if message.media else 0
    document_bonus = 3 if getattr(message, "document", None) else 0
    views = int(getattr(message, "views", 0) or 0)
    reacts = reaction_count(message)
    return len(hits) * 5 + min(views // 100, 30) + min(reacts * 2, 30) + media_bonus + document_bonus, hits


async def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    api_id, api_hash, phone = parse_credentials(TOKEN_FILE.read_text(encoding="utf-8", errors="ignore"))
    client = TelegramClient(str(SESSION), api_id, api_hash)
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        code = os.environ.get("TELEGRAM_CODE")
        if not code:
            print("OTP_REQUIRED")
            await client.disconnect()
            return
        try:
            await client.sign_in(phone=phone, code=code)
        except SessionPasswordNeededError:
            password = os.environ.get("TELEGRAM_2FA_PASSWORD")
            if not password:
                print("TWO_FA_REQUIRED")
                await client.disconnect()
                return
            await client.sign_in(password=password)

    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    dialogs = []
    candidates = []
    async for dialog in client.iter_dialogs(limit=300):
        entity = dialog.entity
        title = dialog.name or ""
        is_groupish = bool(getattr(entity, "megagroup", False) or getattr(entity, "broadcast", False) or dialog.is_group or dialog.is_channel)
        if not is_groupish:
            continue
        title_low = title.lower()
        title_hits = [k for k in KEYWORDS if k in title_low]
        dialogs.append({
            "title": title,
            "id": int(dialog.id),
            "unread": int(dialog.unread_count or 0),
            "title_hits": title_hits,
        })
        if title_hits:
            try:
                async for msg in client.iter_messages(entity, limit=80):
                    if not msg or not msg.date:
                        continue
                    msg_date = msg.date if msg.date.tzinfo else msg.date.replace(tzinfo=timezone.utc)
                    if msg_date < cutoff:
                        continue
                    sc, hits = score_message(msg, title)
                    if sc <= 0:
                        continue
                    candidates.append({
                        "chat_title": title,
                        "chat_id": int(dialog.id),
                        "message_id": int(msg.id),
                        "date": msg_date.isoformat(),
                        "views": int(getattr(msg, "views", 0) or 0),
                        "forwards": int(getattr(msg, "forwards", 0) or 0),
                        "reactions": reaction_count(msg),
                        "has_media": bool(msg.media),
                        "has_document": bool(getattr(msg, "document", None)),
                        "score": sc,
                        "hits": hits,
                        "text_preview": compact_text(msg.message),
                    })
            except Exception as exc:
                candidates.append({
                    "chat_title": title,
                    "chat_id": int(dialog.id),
                    "error": type(exc).__name__,
                    "score": -1,
                })

    candidates.sort(key=lambda x: (x.get("score", 0), x.get("views", 0), x.get("reactions", 0)), reverse=True)
    dialogs.sort(key=lambda x: (len(x["title_hits"]), x["unread"]), reverse=True)
    result = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "dialogs_seen": len(dialogs),
        "matching_dialogs": [d for d in dialogs if d["title_hits"]][:80],
        "top_candidates": candidates[:80],
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "authorized": True,
        "dialogs_seen": result["dialogs_seen"],
        "matching_dialogs": len(result["matching_dialogs"]),
        "top_candidates": len(result["top_candidates"]),
        "output": str(OUT),
    }, ensure_ascii=False))
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
