python3 << 'PYEOF'
code = '''
import asyncio, json, re, os, requests
from bs4 import BeautifulSoup
from groq import AsyncGroq

MODEL = "llama-3.3-70b-versatile"

def _client():
    return AsyncGroq(api_key=os.environ["GROQ_API_KEY"])

async def _llm(system, user, temperature=0.3):
    r = await _client().chat.completions.create(
        model=MODEL,
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=temperature, max_tokens=600)
    return r.choices[0].message.content.strip()

async def _json(system, user):
    raw = await _llm(system+"\\n\\nRespond ONLY with valid JSON. No markdown.", user)
    clean = re.sub(r"```json|```","",raw).strip()
    try:
        return json.loads(clean)
    except:
        m = re.search(r"\\{.*\\}", clean, re.DOTALL)
        if m:
            try:
                return json.loads(m.group())
            except:
                pass
        return {"raw": raw}

def scrape_marine_traffic():
    """
    Scrapes MarineTraffic news for real-time shipping disruption signals.
    Returns list of recent news headlines and summaries.
    Falls back to simulated data if scraping fails.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        url = "https://www.marinetraffic.com/en/ais/details/ships/straits"
        news_items = []

        # Try MarineTraffic blog for shipping news
        blog_url = "https://www.marinetraffic.com/blog/"
        r = requests.get(blog_url, headers=headers, timeout=8)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            articles = soup.find_all("article", limit=5)
            for a in articles:
                title = a.find("h2") or a.find("h3") or a.find("h1")
                if title:
                    news_items.append({
                        "source": "MarineTraffic",
                        "headline": title.get_text(strip=True)[:200],
                        "type": "shipping_news"
                    })

        # Also scrape Lloyd\'s List for Hormuz news
        lloyds_url = "https://lloydslist.maritimeintelligence.informa.com/"
        r2 = requests.get(lloyds_url, headers=headers, timeout=8)
        if r2.status_code == 200:
            soup2 = BeautifulSoup(r2.text, "lxml")
            headlines = soup2.find_all(["h2","h3"], limit=5)
            for h in headlines:
                text = h.get_text(strip=True)
                if len(text) > 20:
                    news_items.append({
                        "source": "LloydsList",
                        "headline": text[:200],
                        "type": "maritime_intelligence"
                    })

        if news_items:
            return {
                "status": "live",
                "source": "MarineTraffic + LloydsListI",
                "items": news_items[:6],
                "timestamp": __import__("datetime").datetime.utcnow().isoformat()
            }
        else:
            raise Exception("No items scraped")

    except Exception as e:
        # Fallback: return simulated Hormuz disruption data
        return {
            "status": "simulated",
            "source": "Aegis Internal Feed",
            "note": f"Live scrape failed ({str(e)[:50]}), using crisis simulation data",
            "items": [
                {"source": "MarineTraffic", "headline": "3 tankers rerouted away from Strait of Hormuz amid escalating tensions", "type": "shipping_disruption"},
                {"source": "MarineTraffic", "headline": "Iranian Revolutionary Guard patrol boats spotted near major shipping lanes", "type": "security_alert"},
                {"source": "LloydsListI", "headline": "War risk insurance premiums surge 40% for Gulf vessels", "type": "financial_impact"},
                {"source": "LloydsListI", "headline": "Major shipping lines suspend bookings through Hormuz indefinitely", "type": "operational_disruption"},
            ],
            "timestamp": __import__("datetime").datetime.utcnow().isoformat()
        }

async def signal_agent(event):
    # Enrich event with live MarineTraffic data
    marine_data = scrape_marine_traffic()
    event["marine_traffic"] = marine_data

    r = await _json("""You are the Signal Agent for Aegis. Classify incoming signals.
You have access to live MarineTraffic shipping news.
Return JSON: severity(LOW|MEDIUM|HIGH|CRITICAL), signal_type, anomalies(list),
confidence(0-100), summary(1 sentence), shipping_alerts(list of strings from marine data).""",
    f"Event: {json.dumps(event)}")
    r["agent"] = "signal"
    r["marine_data"] = marine_data
    return r

async def intelligence_agent(signal, event):
    r = await _json("""You are the Intelligence Agent for Aegis. Interpret signals for business risk.
Return JSON: root_cause, affected_regions(list), supply_chain_impact(LOW|MEDIUM|HIGH|SEVERE),
escalation_probability(0-100), geopolitical_context(1-2 sentences), time_to_impact_days(int).""",
    f"Signal: {json.dumps(signal)}\\nEvent: {json.dumps(event)}")
    r["agent"] = "intelligence"
    return r

async def forecast_agent(intel, forecast_data):
    r = await _json("""You are the Forecast Agent for Aegis. Interpret ML forecasts in business terms.
Return JSON: oil_outlook(string), price_trajectory(RISING|STABLE|FALLING|VOLATILE),
supply_risk_score(0-100), delay_probability(0-100), cost_impact_pct(float),
confidence_level(LOW|MEDIUM|HIGH), key_assumptions(list).""",
    f"Intel: {json.dumps(intel)}\\nML summary: {json.dumps(forecast_data.get(\'summary\',{}))}")
    r["agent"] = "forecast"
    r["ml_summary"] = forecast_data.get("summary",{})
    r["ml_forecast"] = forecast_data.get("forecast",[])[:14]
    return r

async def simulation_agent(forecast, event):
    r = await _json("""You are the Simulation Agent for Aegis. Run 3 supply chain scenarios.
Return JSON: scenarios(list of: name,probability,cost_impact_pct,lead_time_increase_days,description,mitigation_available).""",
    f"Forecast: {json.dumps(forecast)}\\nEvent: {json.dumps(event)}")
    r["agent"] = "simulation"
    if "scenarios" not in r or not isinstance(r["scenarios"], list):
        r["scenarios"] = []
    return r

async def decision_agent(simulation, forecast, intel):
    r = await _json("""You are the Decision Agent for Aegis — the final brain.
Return JSON: threat_level(LOW|MEDIUM|HIGH|CRITICAL),
recommended_actions(list of: priority,action,rationale,estimated_savings_usd,time_to_implement,risk),
executive_summary(2-3 sentences), do_nothing_cost_usd(int).""",
    f"Scenarios: {json.dumps(simulation.get(\'scenarios\',[]))}\\nForecast: {json.dumps(forecast.get(\'ml_summary\',{}))}\\nIntel: {json.dumps(intel)}")
    r["agent"] = "decision"
    return r

async def alert_agent(decision, forecast):
    r = await _json("""You are the Alert Agent for Aegis. Generate stakeholder alerts.
Return JSON: slack_message(string,max 200 chars), email_subject, email_body(3-4 sentences),
severity_emoji, notification_channels(list).""",
    f"Decision: {json.dumps(decision)}\\nForecast: {json.dumps(forecast.get(\'ml_summary\',{}))}")
    r["agent"] = "alert"
    return r

async def execution_agent(decision):
    r = await _json("""You are the Execution Agent for Aegis. Determine workflows to trigger.
Return JSON: triggered_workflows(list of: system,action,api_endpoint,payload_summary,status,requires_human_approval),
autonomous_actions_count(int), pending_approvals_count(int), execution_summary(1 sentence).""",
    f"Actions: {json.dumps(decision.get(\'recommended_actions\',[])[:3])}")
    r["agent"] = "execution"
    return r

async def run_aegis_pipeline(event, forecast_data):
    results = {"event": event, "agents": {}}
    sig   = await signal_agent(event)
    results["agents"]["signal"] = sig
    intel = await intelligence_agent(sig, event)
    results["agents"]["intelligence"] = intel
    fore  = await forecast_agent(intel, forecast_data)
    results["agents"]["forecast"] = fore
    sim   = await simulation_agent(fore, event)
    results["agents"]["simulation"] = sim
    dec   = await decision_agent(sim, fore, intel)
    results["agents"]["decision"] = dec
    alert = await alert_agent(dec, fore)
    results["agents"]["alert"] = alert
    exe   = await execution_agent(dec)
    results["agents"]["execution"] = exe
    print("Pipeline complete")
    return results
'''
with open("/opt/aegis/agents/swarm.py","w") as f:
    f.write(code)
print("swarm.py written OK")
PYEOF

✅ Should print: swarm.py written OK
