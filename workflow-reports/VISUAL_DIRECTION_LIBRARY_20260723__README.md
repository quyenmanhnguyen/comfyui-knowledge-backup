# Visual Direction Library — 2026-07-23

Đây là thư viện chuẩn thị giác, không phải bảng xếp hạng theo tốc độ hoặc theo độ mới.

## Cách dùng

- `APPROVED`: ảnh được giữ làm chuẩn hướng hình ảnh và nguồn đối chiếu trước khi tạo lượt mới.
- `REJECTED_REFERENCES`: ảnh người dùng đã chỉ rõ là mềm/nhòe/không đẹp. Không dùng các ảnh này làm baseline dù workflow hoàn thành.
- `EMBEDDED_WORKFLOWS`: prompt/workflow JSON trích trực tiếp từ metadata PNG tương ứng.
- `manifest.json`: danh sách ảnh, kích thước và metadata đã trích.

## Tiêu chuẩn ưu tiên

Ảnh đạt phải có mặt rõ và có sức sống, da có chuyển sắc/texture thật, mắt tóc và mép trang phục tách bạch, ánh sáng sáng dịu nhưng không rửa mất chi tiết, tay chân hợp lý và bố cục có chủ ý.

Loại ảnh khi có một hoặc nhiều dấu hiệu: mặt mềm như bị lọc beauty, da bệt/sáp, chi tiết tóc và vải tan vào nhau, ánh sáng cửa sổ làm cháy/rửa da, biểu cảm vô hồn, hình thể quá generic, hoặc chỉ “sạch” nhưng thiếu ấn tượng.

## Quy tắc vận hành lần sau

1. Chọn baseline gần nhất trong `APPROVED`.
2. Dùng workflow trích từ chính PNG đó; không dựng lại bằng graph chung.
3. Giữ prompt, seed, canvas, sampler và model ở lượt phục hồi đầu tiên.
4. Chỉ thay một biến ở mỗi A/B.
5. So cạnh baseline và kiểm tra ở kích thước thật.
6. Nếu kết quả giống nhóm `REJECTED_REFERENCES`, loại ngay, không đưa vào báo cáo chính.

