# Nguồn và quyết định test

| Nhánh | Nguồn | Cấu hình lõi | Quyết định |
|---|---|---|---|
| Moody Anima v1 | Civitai model 2700077 + workflow 2700120, Telegram export | ER-SDE/simple, 4 bước, native | Chạy cặp SFW/NSFW |
| Ri-mix α Anima | Civitai model 996220, version 3011920 | Anima base, LoRA 0.70, ER-SDE/simple, 32 bước, CFG 3 | Chạy cặp SFW/NSFW |
| aMix + Ri-mix Ω v2 | Civitai version 2811751 + local proven graph | LoRA 0.65, Euler A/normal, 30 bước, CFG 7 | Chạy cặp SFW/NSFW |
| OneObsession v23 | Civitai model 1318945, version 3118448 + local proven graph | DPM++ 2M/Karras, 32 bước, CFG 5.5 | Chạy cặp SFW/NSFW |

Prompt lấy cấu trúc điện ảnh từ Telegram: tách foreground/midground/background,
motivated key light, rim/fill, color temperature, lens, depth, film grain và
halation. Không sao chép các cảnh quá phức tạp, nội dung không rõ tuổi hoặc pose
dễ sinh thừa chi; mọi nhân vật đều được khóa là người trưởng thành.

Không dùng upscale, hires fix, refiner, Detail Daemon, YOLO/SAM hay face detailer
trong vòng so sánh này.
