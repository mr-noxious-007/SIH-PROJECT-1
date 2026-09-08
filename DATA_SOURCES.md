# Data Sources & Providers (Real-Time Architecture)

This document tracks exactly where data originates, whether an API key/licence is required, and how the FreightIQ engine switches between Live and Fallback instances automatically.

| Feature / Metadata Layer | Priority 1 Source (Live) | API / Endpoint | Update Frequency | Requires Key/Licence | Fallback Mode | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Vessel AIS / Supply** | VesselFinder | `/vessels` API | Near Real-Time | **YES** | Local DB / Hybrid Rule | **HYBRID** |
| **Global Weather** | Open-Meteo | `api.open-meteo.com` | Near Real-Time | NO (Free Open API) | Default 50 Risk | **LIVE** |
| **Macro GDP** | World Bank API | `/v2/country/...` | Annual / Quarterly | NO (Free Open API) | Fixed 3.0% growth | **LIVE** |
| **Port Congestion** | Port Authority Feeds | Official Endpoints | Daily | **YES** / Varies | Static 30% Index | **HYBRID** |
| **Fuel / Bunker Prices** | EIA / Bunkerworld | Provider Auth Endpoint | Daily | **YES** | VLSFO Baseline $600 | **HYBRID** |
| **Freight Benchmark** | Baltic Exchange | Provider Auth Endpoint | Daily | **YES (Licence)** | $12.50 Spot Base | **HYBRID** |
| **Canal Restrictions** | SCA / Panama Configs | Authority Circulars | Real-Time Bulletins | NO (Web Monitor) | Fixed Status `10` | **HYBRID** |

---

### Configuration Strategy
If an environment variable like `VESSELFINDER_API_KEY` is not present in `.env`, the pipeline gracefully downgrades the specific variable layer to `FALLBACK_MODE`. Live Variables (like Weather and GDP) will continue returning live variables. The frontend dynamically informs the user under `Metadata Quality`.

***Rule:*** The engine will NEVER fabricate an AIS position if the API is restricted—it explicitly alerts the user with `UNAVAILABLE`.
