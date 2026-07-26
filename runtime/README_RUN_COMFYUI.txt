ComfyUI Windows AMD ROCm - cach chay gon

1) Chay:
   C:\AI\START_COMFYUI.bat

   Neu ComfyUI da chay san o http://127.0.0.1:8188 thi file nay chi mo web,
   khong start them ban thu hai nua.

2) Tat sach:
   C:\AI\STOP_COMFYUI.bat

3) Khoi dong lai:
   C:\AI\RESTART_COMFYUI.bat

4) Workflow tot da test:
   C:\AI\workflows\KEEP_MAIN_20260713

5) Log start moi:
   C:\AI\logs\comfyui_start.out.log
   C:\AI\logs\comfyui_start.err.log

Ghi chu:
- Port dung mac dinh: 8188.
- Loi cu "Port 8188 already in use" da duoc chan trong START_COMFYUI.
- ComfyUI-Manager da set network_mode=local va channel_url=default de tranh loi invalid channel khi start.
- Canh bao TritonVAE cua KJNodes la optional, khong lam hong server.
