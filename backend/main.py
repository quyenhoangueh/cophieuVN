import os
import requests
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# Tạo app FastAPI
app = FastAPI()

# Cho phép CORS (để frontend Netlify gọi được API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lấy token Fireant từ biến môi trường
FIREANT_TOKEN = os.getenv("FIREANT_TOKEN")
if not FIREANT_TOKEN:
    raise ValueError("⚠ FIREANT_TOKEN chưa được thiết lập trong Render Environment Variables")

# Hàm lấy quote từ Fireant
def get_quote(ticker: str):
    url = f"https://restv2.fireant.vn/symbols/{ticker}"
    headers = {"Authorization": f"Bearer {FIREANT_TOKEN}"}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

# API endpoint: /api/quotes?tickers=VNM,HPG
@app.get("/api/quotes")
def quotes(tickers: str = Query(..., description="Danh sách mã, ví dụ: VNM,HPG,GEX")):
    tickers_list = [t.strip().upper() for t in tickers.split(",")]
    results = []
    for t in tickers_list:
        try:
            data = get_quote(t)
            results.append({"ticker": t, "data": data})
        except Exception as e:
            results.append({"ticker": t, "error": str(e)})
    return results

# Root test
@app.get("/")
def root():
    return {"status": "ok", "message": "AIoT Screener Backend is running"}
