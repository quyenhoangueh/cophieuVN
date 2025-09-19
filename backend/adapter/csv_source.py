
import csv
from typing import List, Dict

class CsvSource:
    def __init__(self, path: str = "data.csv"):
        self.path = path

    def _read_all(self) -> Dict[str, Dict]:
        out = {}
        try:
            with open(self.path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    t = (row.get("ticker") or "").strip().upper()
                    if not t:
                        continue
                    def fnum(k, d=0):
                        v = row.get(k)
                        try:
                            return float(str(v).replace(",","")) if v not in (None,"") else d
                        except:
                            return d
                    out[t] = {
                        "ticker": t,
                        "price": fnum("price"),
                        "changePct1D": fnum("changePct1D"),
                        "changePct5D": fnum("changePct5D"),
                        "changePct20D": fnum("changePct20D"),
                        "liquidity_bnVND": fnum("liquidity_bnVND"),
                        "VolSurge": fnum("VolSurge"),
                        "PE": fnum("PE"),
                        "PB": fnum("PB"),
                        "ROE": fnum("ROE"),
                        "EPSYoY": fnum("EPSYoY"),
                        "RevGrowthYoY": fnum("RevGrowthYoY"),
                        "ForeignNetBn_bnVND": fnum("ForeignNetBn_bnVND"),
                        "NewHigh52W": str(row.get("NewHigh52W","")).strip().lower() in ("true","1","yes","y","x")
                    }
        except FileNotFoundError:
            pass
        return out

    def get_quotes(self, tickers: List[str]) -> List[Dict]:
        data = self._read_all()
        return [{k: v.get(k) for k in ["ticker","price","changePct1D","changePct5D","changePct20D","liquidity_bnVND","VolSurge"]} 
                if (v := data.get(t)) else {"ticker": t, "price":0,"changePct1D":0,"changePct5D":0,"changePct20D":0,"liquidity_bnVND":0,"VolSurge":0}
                for t in tickers]

    def get_fundamentals(self, tickers: List[str]) -> List[Dict]:
        data = self._read_all()
        return [{k: v.get(k) for k in ["ticker","PE","PB","ROE","EPSYoY","RevGrowthYoY","ForeignNetBn_bnVND","NewHigh52W"]}
                if (v := data.get(t)) else {"ticker": t, "PE":0,"PB":0,"ROE":0,"EPSYoY":0,"RevGrowthYoY":0,"ForeignNetBn_bnVND":0,"NewHigh52W":False}
                for t in tickers]
