import os
from typing import List, Dict
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from adapter.csv_source import CsvSource
from adapter.fireant import FireAntSource

app = FastAPI(title="AIoT Screener — CANSLIM Live")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

def get_source():
    token = os.getenv("FIREANT_TOKEN", "").strip()
    if token:
        return FireAntSource(token)
    return CsvSource(os.getenv("CSV_PATH", "data.csv"))

@app.get("/api/quotes")
def quotes(tickers: str = Query(...)) -> List[Dict]:
    src = get_source()
    return src.get_quotes([t.strip().upper() for t in tickers.split(",") if t.strip()])

@app.get("/api/fundamentals")
def fundamentals(tickers: str = Query(...)) -> List[Dict]:
    src = get_source()
    return src.get_fundamentals([t.strip().upper() for t in tickers.split(",") if t.strip()])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
