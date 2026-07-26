import asyncio
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.tl.functions.messages import GetForumTopicsRequest


TOKEN_FILE = Path(os.environ.get("TELEGRAM_TOKEN_FILE", r"REPLACE_WITH_LOCAL_TOKEN_FILE.txt"))
SESSION = os.environ.get("TELEGRAM_SESSION", r"C:\AI\telegram_client\comfyui_readonly")
OUT = Path(os.environ.get("MOODY_SCAN_OUT", r"C:\AI\telegram_client\moody_realtime_scan.json"))
GROUP_HINTS = ["Moody", "小圆脸", "同好会"]
TOPIC_KEEP = ["model", "Sharing", "Prompts", "提示", "分享", "模型", "English", "Q&A"]
KEYWORDS = [
    "z-image", "z image", "zimage", "moody", "sdxl", "illustrious", "anima",
    "comfy", "workflow", "lora", "checkpoint", "sampler", "steps", "cfg",
    "prompt", "vae", "qwen", "flux", "模型", "工作流", "提示词", "采样", "节点",
]


def parse_credentials(text):
    api_id = int(re.search(r"\b(\d{5,})\b", text).group(1))
    api_hash = re.search(r"\b([a-fA-F0-9]{32})\b", text).group(1)
    phone_m = re.search(r"(\+\d[\d\s-]{7,}\d)", text)
    phone = re.sub(r"[\s-]+", "", phone_m.group(1)) if phone_m else None
    return api_id, api_hash, phone


def reaction_count(message):
    r = getattr(message, "reactions", None)
    if not r or not getattr(r, "results", None):
        return 0
    return sum(int(getattr(x, "count", 0) or 0) for x in r.results)


def compact(text, n=900):
    return re.sub(r"\s+", " ", text or "").strip()[:n]


def file_names(message):
    names = []
    doc = getattr(message, "document", None)
    if doc:
        for attr in getattr(doc, "attributes", []) or []:
            name = getattr(attr, "file_name", None)
            if name:
                names.append(name)
    return names


def score(message, topic_title):
    text = message.message or ""
    blob = (topic_title + " " + text + " " + " ".join(file_names(message))).lower()
    hits = [k for k in KEYWORDS if k in blob]
    views = int(getattr(message, "views", 0) or 0)
    reacts = reaction_count(message)
    media_bonus = 3 if getattr(message, "media", None) else 0
    file_bonus = 5 if file_names(message) else 0
    return len(hits) * 8 + min(views // 50, 40) + min(reacts * 3, 45) + media_bonus + file_bonus, hits


async def main():
    api_id, api_hash, phone = parse_credentials(TOKEN_FILE.read_text(encoding="utf-8", errors="ignore"))
    client = TelegramClient(SESSION, api_id, api_hash)
    await client.start(phone=phone)

    target = None
    async for dialog in client.iter_dialogs(limit=500):
        title = dialog.name or ""
        if all(h.lower() in title.lower() for h in ["moody"]) or any(h in title for h in GROUP_HINTS):
            target = dialog.entity
            group_title = title
            break
    if target is None:
        raise RuntimeError("Moody group not found")

    topics_res = await client(GetForumTopicsRequest(peer=target, offset_date=0, offset_id=0, offset_topic=0, limit=80, q=""))
    topics = []
    for topic in topics_res.topics:
        title = topic.title or ""
        if any(k.lower() in title.lower() for k in TOPIC_KEEP):
            topics.append({"id": topic.id, "title": title, "unread": getattr(topic, "unread_count", None), "top_message": topic.top_message})

    cutoff = datetime.now(timezone.utc) - timedelta(days=10)
    rows = []
    for topic in topics:
        try:
            async for msg in client.iter_messages(target, limit=120, reply_to=topic["id"]):
                if not msg or not msg.date:
                    continue
                d = msg.date if msg.date.tzinfo else msg.date.replace(tzinfo=timezone.utc)
                if d < cutoff:
                    continue
                sc, hits = score(msg, topic["title"])
                if sc < 8 and not getattr(msg, "media", None):
                    continue
                rows.append({
                    "group": group_title,
                    "topic": topic["title"],
                    "topic_id": topic["id"],
                    "message_id": msg.id,
                    "date": d.isoformat(),
                    "views": int(getattr(msg, "views", 0) or 0),
                    "forwards": int(getattr(msg, "forwards", 0) or 0),
                    "reactions": reaction_count(msg),
                    "has_media": bool(getattr(msg, "media", None)),
                    "files": file_names(msg),
                    "score": sc,
                    "hits": hits,
                    "text_preview": compact(msg.message),
                })
        except Exception as exc:
            rows.append({"topic": topic["title"], "topic_id": topic["id"], "error": type(exc).__name__, "detail": str(exc)[:200]})

    rows.sort(key=lambda x: (x.get("score", 0), x.get("views", 0), x.get("reactions", 0)), reverse=True)
    data = {"scanned_at": datetime.now(timezone.utc).isoformat(), "group": group_title, "topics": topics, "top_messages": rows[:120]}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"group": group_title, "topics": len(topics), "messages": len(rows), "output": str(OUT)}, ensure_ascii=False))
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
