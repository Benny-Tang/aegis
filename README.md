# Aegis — Autonomous Enterprise Crisis Management
**Shield Against Chaos**

Aegis is a 7-agent autonomous pipeline that monitors global shipping
intelligence and commodity markets in real time, forecasts supply-chain
disruption (e.g. a Strait of Hormuz closure), simulates response scenarios,
and recommends ranked, cost-quantified actions — without a human analyst
in the loop.

Built for the AMD Developer Cloud hackathon track (2026), running on
AMD Instinct MI300X GPUs.

## Architecture

```
[MarineTraffic + Lloyd's List]        [Oil price / market data]
              |                                |
              +----------------+---------------+
                               |
                        [Signal Agent]        <- Agent 1: Watcher
                               |
                    [Intelligence Agent]      <- Agent 2: Interpreter
                               |
                      [Forecast Agent]        <- Agent 3: ARIMA + XGBoost
                               |
                     [Simulation Agent]       <- Agent 4: Strategist (3 scenarios)
                               |
                      [Decision Agent]        <- Agent 5: Brain (ranked actions)
                               |
                       [Alert Agent]          <- Agent 6: Communicator
                               |
                     [Execution Agent]        <- Agent 7: Operator (ERP workflows)
                               |
                      [FastAPI + SSE]
                               |
                       [Dashboard UI]
```

## Tech stack

| Layer | Technology | Purpose |
|---|---|---|
| LLM | Groq (`openai/gpt-oss-120b`) | Reasoning for all 7 agents |
| Forecasting | ARIMA(2,1,2) + XGBoost | 14-day oil price + delay prediction |
| GPU | AMD Instinct MI300X | Model inference / forecasting acceleration |
| Backend | FastAPI + Server-Sent Events | Real-time agent streaming |
| Marine intel | MarineTraffic + Lloyd's List scrape | Live shipping disruption signals |
| Frontend | Single-page dashboard (vanilla JS) | Live agent monitor, crisis injection |

## Project structure

```
aegis-amd/
├── agents/
│   └── swarm.py           # 7-agent pipeline logic + 4-source marine scraper
│                           #   (MarineTraffic, gCaptain, TradeWinds, Reuters)
├── api/
│   └── server.py          # FastAPI app: /health, /api/marine, /api/crisis,
│                           #   /api/stream (SSE), /api/status
├── models/
│   └── forecaster.py      # ARIMA(2,1,2) + XGBoost hybrid forecasting model
├── frontend.html           # Dashboard UI: live agents, marine feed,
│                           #   business value panel, GTM strategy panel
├── requirements.txt
└── README.md
```

## Business case (from the original hackathon pitch)

| Metric | Value |
|---|---|
| Total addressable market | $1.5T |
| Supply chain market (2028) | $19.3T |
| Estimated ROI, year 1 | 70x |
| Savings per crisis prevented | $1.7M |
| Annual subscription (proposed) | $24K/yr |
| Response time vs. human analysts | 2 sec vs. 4–8 hours |

Target segments: maritime insurance underwriters, commodity traders,
manufacturers with $50M+ procurement exposure, and sovereign wealth funds
managing oil-revenue exposure.

## Running locally

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000` for the live dashboard. Click **Inject Crisis
Scenario** to trigger the full 7-agent pipeline against a simulated Strait
of Hormuz disruption event.

## API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | System status, model, platform info |
| `/api/marine` | GET | Live MarineTraffic + Lloyd's List shipping feed |
| `/api/forecast` | POST | Run the forecasting model standalone |
| `/api/crisis` | POST | Run the full 7-agent pipeline synchronously |
| `/api/stream` | GET | Run the pipeline via Server-Sent Events (used by the dashboard) |
| `/api/status` | GET | Live oil price + system status snapshot |

## License

MIT
