python3 << 'PYEOF'
code = '''
import asyncio, json, os, sys, time
from datetime import datetime
from typing import AsyncGenerator
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

sys.path.insert(0, "/opt/aegis")
from agents.swarm import (signal_agent, intelligence_agent, forecast_agent,
    simulation_agent, decision_agent, alert_agent, execution_agent,
    run_aegis_pipeline, scrape_marine_traffic)
from models.forecaster import get_forecaster

app = FastAPI(title="Aegis", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Response-Time"] = f"{round((time.time()-start)*1000,1)}ms"
    response.headers["X-Powered-By"] = "AMD Instinct MI300X"
    return response

class CrisisEvent(BaseModel):
    oil_price_change_pct: float = Field(default=18.0)
    shipping_disruption:  str   = Field(default="Strait of Hormuz disruption")
    news_headline:        str   = Field(default="Regional conflict near Persian Gulf")
    severity:             str   = Field(default="HIGH")
    disruption_factor:    float = Field(default=0.7, ge=0, le=1)
    horizon_days:         int   = Field(default=14, ge=1, le=90)

class ForecastRequest(BaseModel):
    oil_shock_pct:     float = Field(default=0.0)
    disruption_factor: float = Field(default=0.0, ge=0, le=1)
    horizon_days:      int   = Field(default=14, ge=1, le=90)

@app.on_event("startup")
async def startup():
    print("Aegis starting on AMD Developer Cloud...")
    try:
        get_forecaster()
        print("Forecaster ready")
    except Exception as e:
        print(f"Forecaster warning: {e}")

@app.get("/health")
async def health():
    return {
        "status": "online", "system": "Aegis", "version": "2.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": 7, "platform": "AMD Developer Cloud",
        "model": "llama-3.3-70b-versatile",
        "forecast": "ARIMA(2,1,2) + XGBoost hybrid",
    }

@app.get("/api/marine")
async def marine_feed():
    """Live MarineTraffic shipping news feed."""
    try:
        data = scrape_marine_traffic()
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/forecast")
async def forecast_only(req: ForecastRequest):
    try:
        fc = get_forecaster()
        result = fc.forecast(req.horizon_days, req.oil_shock_pct, req.disruption_factor)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/crisis")
async def run_crisis(event: CrisisEvent):
    try:
        fc = get_forecaster()
        forecast_data = fc.forecast(event.horizon_days, event.oil_price_change_pct, event.disruption_factor)
        results = await run_aegis_pipeline(event.model_dump(), forecast_data)
        return {"success": True, "timestamp": datetime.utcnow().isoformat(), "data": results}
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"{e}\\n{traceback.format_exc()}")

@app.get("/api/stream")
async def stream_crisis(oil_change: float=18.0, disruption: float=0.7, severity: str="HIGH"):
    async def gen() -> AsyncGenerator[str, None]:
        def sse(d): return f"data: {json.dumps(d)}\\n\\n"
        yield sse({"type":"start","message":"Aegis pipeline initiated"})
        try:
            fc = get_forecaster()
            fd = fc.forecast(14, oil_change, disruption)
            yield sse({"type":"forecast_ready","data":fd["summary"]})
            ev = {"oil_price_change_pct":oil_change,"shipping_disruption":"Strait of Hormuz",
                  "news_headline":"Geopolitical escalation","severity":severity,"disruption_factor":disruption}
            yield sse({"type":"agent_start","agent":"signal","index":1})
            sig = await signal_agent(ev)
            yield sse({"type":"agent_done","agent":"signal","data":sig})
            yield sse({"type":"agent_start","agent":"intelligence","index":2})
            intel = await intelligence_agent(sig, ev)
            yield sse({"type":"agent_done","agent":"intelligence","data":intel})
            yield sse({"type":"agent_start","agent":"forecast","index":3})
            fore = await forecast_agent(intel, fd)
            yield sse({"type":"agent_done","agent":"forecast","data":fore})
            yield sse({"type":"agent_start","agent":"simulation","index":4})
            sim = await simulation_agent(fore, ev)
            yield sse({"type":"agent_done","agent":"simulation","data":sim})
            yield sse({"type":"agent_start","agent":"decision","index":5})
            dec = await decision_agent(sim, fore, intel)
            yield sse({"type":"agent_done","agent":"decision","data":dec})
            yield sse({"type":"agent_start","agent":"alert","index":6})
            alert = await alert_agent(dec, fore)
            yield sse({"type":"agent_done","agent":"alert","data":alert})
            yield sse({"type":"agent_start","agent":"execution","index":7})
            exe = await execution_agent(dec)
            yield sse({"type":"agent_done","agent":"execution","data":exe})
            yield sse({"type":"complete","message":"All 7 agents finished",
                       "summary":dec.get("executive_summary",""),"threat":dec.get("threat_level","")})
        except Exception as e:
            yield sse({"type":"error","message":str(e)})
    return StreamingResponse(gen(), media_type="text/event-stream",
                             headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

@app.get("/api/status")
async def status():
    import random
    return {"agents_online":7,"platform":"AMD Developer Cloud",
            "oil_price":round(82+random.uniform(-2,2),2),
            "risk_level":"LOW","groq_model":"llama-3.3-70b-versatile",
            "forecast_model":"ARIMA(2,1,2)+XGBoost"}

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("/opt/aegis/frontend.html") as f:
        return f.read()
'''
with open("/opt/aegis/api/server.py","w") as f:
    f.write(code)
print("server.py written OK")
PYEOF

✅ Should print: server.py written OK
