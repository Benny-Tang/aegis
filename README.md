# 🛡️ Aegis — Autonomous Enterprise Crisis Management

> **AMD Developer Hackathon 2026** | Track 1: AI Agents & Agentic Workflows

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green.svg)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3%2070B-orange.svg)](https://groq.com)
[![AMD](https://img.shields.io/badge/GPU-AMD%20Instinct%20MI300X-red.svg)](https://amd.com)

**Aegis** is a fully autonomous 7-agent AI system that monitors global supply chain risks in real time, predicts disruptions using a hybrid ML forecasting model, and autonomously executes crisis response decisions — before humans can react.

> *"Aegis protects enterprises from global disruptions by turning real-time chaos into autonomous decisions."*

---

## 🎬 Live Demo

| | |
|---|---|
| **Live App** | http://165.245.140.165:8000/ |
| **Demo Video** | https://youtube.com/YOUR_VIDEO_LINK |
| **API Docs** | https://YOUR_AMD_INSTANCE_IP/docs |

---

## 🧠 How It Works

When a crisis event is detected (oil price spike, shipping disruption, geopolitical escalation), Aegis activates a chain of 7 specialized AI agents that reason, forecast, simulate, decide, and act — autonomously.

```
Crisis Event Detected
        │
        ▼
┌───────────────────────────────────────────────────┐
│              AEGIS 7-AGENT PIPELINE               │
│                                                   │
│  📡 Signal Agent     → Detects anomalies          │
│  🧠 Intelligence Agent → Interprets risk context  │
│  📈 Forecast Agent   → ARIMA + XGBoost prediction │
│  🧩 Simulation Agent → Runs what-if scenarios     │
│  ⚡ Decision Agent   → Ranks action plan          │
│  🚨 Alert Agent      → Dispatches notifications   │
│  🔄 Execution Agent  → Triggers workflows         │
└───────────────────────────────────────────────────┘
        │
        ▼
  Autonomous Response
  (Recommendations + Actions in ~4 seconds)
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Groq — LLaMA 3.3 70B Versatile |
| **ML Forecast** | XGBoost 2.0 + ARIMA(2,1,2) hybrid ensemble |
| **GPU Acceleration** | AMD Instinct MI300X via ROCm |
| **API** | FastAPI + Uvicorn + Gunicorn (4 workers) |
| **Streaming** | Server-Sent Events (SSE) — live agent updates |
| **Deployment** | AMD Developer Cloud (amd.digitalocean.com) |
| **Frontend** | Vanilla JS + CSS — dark terminal aesthetic |

---

## 🚀 Quick Start

### Option A — Google Colab (easiest)
1. Open `Aegis_Hackathon.ipynb` in Google Colab
2. Fill in your `GROQ_API_KEY` and `NGROK_TOKEN` in Cell 1
3. Click **Runtime → Run All**
4. Copy the ngrok URL printed at the bottom

### Option B — AMD Developer Cloud (production)
```bash
# 1. SSH into your AMD MI300X instance
ssh -i your-key.pem ubuntu@YOUR_AMD_IP

# 2. Run setup (one command)
chmod +x deploy/setup_amd.sh && ./deploy/setup_amd.sh

# 3. Upload project files
scp -r ./aegis/* ubuntu@YOUR_AMD_IP:/opt/aegis/

# 4. Set API key and start
export GROQ_API_KEY="gsk_YOUR_KEY"
chmod +x deploy/start.sh && ./deploy/start.sh start

# 5. Open in browser — works for unlimited concurrent viewers
http://YOUR_AMD_IP
```

---

## 📁 Project Structure

```
aegis/
├── agents/
│   └── swarm.py              # 7 Groq-powered autonomous agents
├── models/
│   └── forecaster.py         # ARIMA + XGBoost hybrid ML model
├── api/
│   └── server.py             # FastAPI + SSE streaming server
├── deploy/
│   ├── setup_amd.sh          # AMD cloud one-command setup
│   ├── start.sh              # Start / stop / status / logs
│   └── benchmark_gpu.py      # MI300X GPU benchmark
├── Aegis_Hackathon.ipynb     # Google Colab notebook
├── requirements.txt
└── LICENSE
```

---

## 🤖 The 7 Agents

### 1. 📡 Signal Agent (Watcher)
Monitors real-time feeds — oil prices, shipping routes, geopolitical news. Classifies anomalies by severity (LOW → CRITICAL) and confidence score.

### 2. 🧠 Intelligence Agent (Interpreter)
Uses LLaMA 3.3 70B to convert raw signals into structured risk context. Identifies root causes, affected regions, and escalation probability.

### 3. 📈 Forecast Agent (Predictor)
Runs a **hybrid ARIMA(2,1,2) + XGBoost ensemble** model to predict oil prices, logistics delays, and cost impact over 14 days. XGBoost runs on AMD MI300X GPU via ROCm for accelerated inference.

### 4. 🧩 Simulation Agent (Strategist)
Generates 3 what-if scenarios (best case, base case, worst case) with probability weights and cost impact estimates.

### 5. ⚡ Decision Agent (Brain)
Synthesizes all upstream context into a ranked action plan with estimated savings, implementation timeline, and risk ratings.

### 6. 🚨 Alert Agent (Communicator)
Formats and dispatches real-time alerts to Slack, email, and dashboard. Generates executive summaries for C-suite stakeholders.

### 7. 🔄 Execution Agent (Operator)
Triggers downstream enterprise workflows autonomously — ERP supplier switches, procurement API calls, logistics rerouting.

---

## 📊 ML Forecasting Model

**Why ARIMA + XGBoost hybrid?**

| Component | Role | Weight (crisis) |
|-----------|------|-----------------|
| ARIMA(2,1,2) | Linear trend + autocorrelation | 30% |
| XGBoost (ROCm GPU) | Non-linear geopolitical signals | 70% |

**Features engineered:** lag-1, lag-3, lag-7, lag-14, lag-21, rolling mean/std (7, 14, 21 day), 3-day & 7-day % change, day-of-week, month

**AMD MI300X advantage:** XGBoost tree building runs ~8–15x faster on MI300X vs CPU via ROCm CUDA compatibility layer, enabling real-time batch scenario simulation.

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Live dashboard |
| `GET` | `/health` | System health + GPU status |
| `GET` | `/docs` | Swagger UI |
| `POST` | `/api/crisis` | Full 7-agent pipeline (JSON) |
| `GET` | `/api/stream` | SSE live agent stream |
| `POST` | `/api/forecast` | ML forecast only |
| `GET` | `/api/gpu` | Live MI300X utilization |

### Example — trigger crisis
```bash
curl -X POST http://YOUR_IP/api/crisis \
  -H "Content-Type: application/json" \
  -d '{
    "oil_price_change_pct": 18.0,
    "shipping_disruption": "Strait of Hormuz — 3 tankers rerouted",
    "news_headline": "Regional conflict escalation near Persian Gulf",
    "severity": "HIGH",
    "disruption_factor": 0.7,
    "horizon_days": 14
  }'
```

### Example — SSE stream (JavaScript)
```javascript
const es = new EventSource('http://YOUR_IP/api/stream?oil_change=18&disruption=0.7');
es.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  console.log(msg.type, msg.agent, msg.data);
};
```

---

## 💡 Business Value

Aegis addresses a $1.5 trillion annual problem — global supply chain disruptions caused by geopolitical events, commodity shocks, and logistics failures.

**Key metrics from demo scenario (Strait of Hormuz crisis):**
- ⏱️ Response time: **4 seconds** (vs hours for human analysts)
- 💰 Estimated savings identified: **$1.7M** per crisis event
- 🎯 Forecast accuracy: ARIMA+XGBoost hybrid outperforms either model alone
- 🔄 Agents active simultaneously: **7 / 7**

---

## 🏗️ AMD Developer Cloud Setup

```bash
# Check MI300X is available
rocm-smi

# Run GPU benchmark (show judges real GPU utilization)
python3 deploy/benchmark_gpu.py

# Monitor live
./deploy/start.sh status
./deploy/start.sh logs
```

---

## 📋 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ Yes | Get free at console.groq.com |
| `NGROK_TOKEN` | Colab only | Get free at ngrok.com |

---

## 🙏 Acknowledgements

- **AMD** — MI300X GPU access via AMD Developer Cloud
- **Groq** — Ultra-fast LLaMA 3.3 70B inference
- **lablab.ai** — Hackathon platform and community
- **FastAPI** — Production API framework
- **XGBoost** — GPU-accelerated gradient boosting

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built with ❤️ for the AMD Developer Hackathon 2025*
