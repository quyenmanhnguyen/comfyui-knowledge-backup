# Restore guide

If the local Codex/ComfyUI memory is lost, restore in this order:

1. Copy `skill/` back to:

   `C:\Users\Admin\.codex\skills\optimize-comfyui-rx7800xt`

2. Read these first:

   - `skill/references/machine-profile.md`
   - `skill/references/local-evidence.md`
   - `skill/references/historical-winners.md`
   - `skill/references/recent-two-hour-audit.md`
   - `skill/references/zimage-playbook.md`
   - `skill/references/sdxl-playbook.md`

3. Recreate runtime helpers from `runtime/` only if the local files are missing.

4. Use `inventory/model_inventory.json` and `inventory/custom_nodes.json` to understand what was installed. These are inventories only; the model weights themselves are not stored here.

5. Use `workflow-json/` to recover the known-good workflow graphs and reports. Do not treat every workflow as good; read `local-evidence.md` and the HTML reports for keep/reject labels.

6. For Telegram realtime scanning, use `tooling/telegram_client/`, but provide credentials locally via:

   ```powershell
   $env:TELEGRAM_TOKEN_FILE='C:\path\to\your\token-file.txt'
   ```

   Telegram sessions and OTP state are intentionally not backed up.

7. Never restore by copying this repo over all of `C:\AI`; it is a knowledge backup, not a full ComfyUI installation backup.
