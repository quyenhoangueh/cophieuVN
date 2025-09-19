# AIoT Screener — CANSLIM Live (Sectors, Hardcode backend)

**Backend URL cố định:** https://aiot-screener-backend.onrender.com  
Frontend đã gọi thẳng URL này → bạn và khách không cần nhập gì.

## Deploy nhanh
### Backend (Render)
1. Push repo lên GitHub → Render → New Web Service → chọn repo.
2. Đặt **Service name** = `aiot-screener-backend` (để đúng URL cố định).
3. Thêm env var: `FIREANT_TOKEN = <token FireAnt>` (nếu có).
4. Deploy xong có URL trên.

> Không có token → backend tự đọc file `data.csv` (đặt cạnh `backend/main.py`).

### Frontend (Netlify)
1. Netlify → New site from Git → chọn repo.
2. Xong. Frontend gọi trực tiếp `https://aiot-screener-backend.onrender.com/api/...`.

## Sử dụng
- Trang có **menu chọn ngành** + danh sách mã mặc định (VN30 + midcap phổ biến).
- Bấm **Tải dữ liệu** rồi **CANSLIM** để áp preset.
- Bộ lọc: PE, PB, ROE, EPS YoY, Rev YoY, VolSurge, Thanh khoản.
- **Export CSV** danh sách kết quả.

Ngày build: 2025-09-19
