import asyncio
import json
import os
from pathlib import Path

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

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
    code = os.environ.pop("TELEGRAM_OTP", "").strip().rstrip(".")
    if not code.isdigit():
        raise RuntimeError("OTP must contain digits only")
    raw = SOURCE.read_text(encoding="utf-8-sig")
    lines = raw.splitlines()
    api_id = int(value_after_label(lines, "App api_id"))
    api_hash = value_after_label(lines, "App api_hash")
    state = json.loads(STATE.read_text(encoding="utf-8"))

    client = TelegramClient(str(SESSION), api_id, api_hash)
    await client.connect()
    try:
        await client.sign_in(
            phone=state["phone"],
            code=code,
            phone_code_hash=state["phone_code_hash"],
        )
    except SessionPasswordNeededError:
        print("TWO_FACTOR_PASSWORD_REQUIRED")
        await client.disconnect()
        return

    me = await client.get_me()
    print(f"AUTHORIZED user_id={me.id} username_set={bool(me.username)}")
    STATE.unlink(missing_ok=True)
    await client.disconnect()


asyncio.run(main())
