import asyncio
import json
import os
import re
from pathlib import Path

from telethon import TelegramClient

SOURCE = Path(os.environ.get("TELEGRAM_TOKEN_FILE", r"REPLACE_WITH_LOCAL_TOKEN_FILE.txt"))
ROOT = Path(os.environ.get("TELEGRAM_CLIENT_DIR", r"C:\AI\telegram_client"))
SESSION = ROOT / "personal"
STATE = ROOT / "pending_login.json"


def value_after_label(lines, label):
    for i, line in enumerate(lines):
        if line.strip().lower().rstrip(":=") == label.lower():
            for candidate in lines[i + 1 :]:
                if candidate.strip():
                    return candidate.strip()
    raise RuntimeError(f"Missing {label}")


async def main():
    raw = SOURCE.read_text(encoding="utf-8-sig")
    lines = raw.splitlines()
    api_id = int(value_after_label(lines, "App api_id"))
    api_hash = value_after_label(lines, "App api_hash")
    match = re.search(r"(?im)^\s*TELEGRAM_PHONE\s*[:=]\s*(\+?\d{8,15})\s*$", raw)
    if not match:
        raise RuntimeError("Missing TELEGRAM_PHONE")
    phone = match.group(1)

    client = TelegramClient(str(SESSION), api_id, api_hash)
    await client.connect()
    if await client.is_user_authorized():
        print("ALREADY_AUTHORIZED")
    else:
        sent = await client.send_code_request(phone)
        STATE.write_text(
            json.dumps({"phone": phone, "phone_code_hash": sent.phone_code_hash}),
            encoding="utf-8",
        )
        print(f"OTP_SENT type={type(sent.type).__name__} next_type={type(sent.next_type).__name__ if sent.next_type else 'none'} timeout={sent.timeout}")
    await client.disconnect()


asyncio.run(main())
