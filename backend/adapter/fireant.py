
import requests
from typing import List, Dict

class FireAntSource:
    def __init__(self, token: str):
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})
        self.base = "https://restv2.fireant.vn"

    def _get(self, url, params=None):
        r = self.session.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()

    def get_quotes(self, tickers: List[str]) -> List[Dict]:
        out = []
        for t in tickers:
            try:
                q = self._get(f"{self.base}/symbols/{t}/quote")
                price = q.get("matchPrice") or q.get("price") or q.get("lastPrice")
                pct1d = q.get("rate") or q.get("changePercent") or 0
                vol = q.get("totalVolume") or 0
                val_bn = (q.get("totalValue") or 0)/1e9
                pct5d = q.get("change5dPercent") or 0
                pct20d = q.get("change20dPercent") or 0
                vol_avg20 = q.get("avgVolume20d") or 0
                vol_surge = (vol/vol_avg20) if vol_avg20 else 0
                out.append({
                    "ticker": t,
                    "price": round(float(price or 0),2),
                    "changePct1D": round(float(pct1d or 0),2),
                    "changePct5D": round(float(pct5d or 0),2),
                    "changePct20D": round(float(pct20d or 0),2),
                    "liquidity_bnVND": round(float(val_bn),1),
                    "VolSurge": round(float(vol_surge),2),
                })
            except Exception as e:
                out.append({"ticker": t, "error": str(e)})
        return out

    def get_fundamentals(self, tickers: List[str]) -> List[Dict]:
        out = []
        for t in tickers:
            try:
                fin = self._get(f"{self.base}/symbols/{t}/financials/ratios")
                pe = fin.get("pe") or fin.get("PE") or 0
                pb = fin.get("pb") or fin.get("PB") or 0
                roe = fin.get("roe") or fin.get("ROE") or 0
                growth_rev_yoy = fin.get("revenueYoY") or 0
                eps_yoy = fin.get("epsYoY") or 0
                foreign_net = fin.get("foreignNetValue") or 0
                is52w = bool(fin.get("is52wHigh"))
                out.append({
                    "ticker": t,
                    "PE": float(pe or 0),
                    "PB": float(pb or 0),
                    "ROE": float(roe or 0),
                    "RevGrowthYoY": float(growth_rev_yoy or 0),
                    "EPSYoY": float(eps_yoy or 0),
                    "ForeignNetBn_bnVND": float(foreign_net)/1e9,
                    "NewHigh52W": is52w
                })
            except Exception as e:
                out.append({"ticker": t, "PE":0,"PB":0,"ROE":0,"RevGrowthYoY":0,"EPSYoY":0,"ForeignNetBn_bnVND":0,"NewHigh52W":False,"error":str(e)})
        return out
