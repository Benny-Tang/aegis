# Changelog

## [Unreleased]

### Added
- Test suite: `tests/test_forecaster.py` (forecast horizon, bounds, crisis-shock behavior) and `tests/test_server.py` (health, forecast, status, marine endpoints)
- CI pipeline (`.github/workflows/ci.yml`) running `ruff check` and `pytest` on every push/PR
- `ruff.toml` lint configuration
- `.env.example` documenting required/optional environment variables
- Typed Pydantic response models for all API endpoints (`HealthResponse`, `MarineResponse`, `ForecastResponse`, `CrisisResponse`, `StatusResponse`)
- Structured logging (`logging` module) replacing `print()` statements throughout the API layer

### Changed
- Error responses no longer leak internal tracebacks to clients (`/api/crisis` previously returned `traceback.format_exc()` in the HTTP response body) — full details are now logged server-side only, clients get a generic safe message
- Swapped the decommissioned Groq model `llama-3.3-70b-versatile` for `openai/gpt-oss-120b`
- Converted from hardcoded absolute paths (`/opt/aegis`, `/content/aegis`) to a relative, portable repo structure

### Fixed
- Groq client was previously instantiated fresh on every LLM call; now a single client instance is reused
- MarineTraffic scraper: each source (MarineTraffic, gCaptain, TradeWinds, Reuters) now fails independently instead of one broad try/except covering all sources
- Frontend JS: fixed a malformed string-concatenation bug in the `log()` function that broke the opening `<div>` tag for log entries

## [2.0.0] — initial hackathon submission (AMD Developer Cloud track)

- 7-agent crisis-simulation pipeline (Signal → Intelligence → Forecast → Simulation → Decision → Alert → Execution)
- ARIMA(2,1,2) + XGBoost hybrid forecaster
- FastAPI backend with Server-Sent Events streaming
- Single-page dashboard with live agent monitor, crisis injection, business-value and go-to-market panels
