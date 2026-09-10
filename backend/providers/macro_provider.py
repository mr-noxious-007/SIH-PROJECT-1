import os
import requests
from typing import Dict, Any
from .base_provider import BaseProvider

class MacroProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        
    def get_global_gdp_growth(self) -> Dict[str, Any]:
        """
        Uses World Bank API (Free, Public, no auth required for basic data)
        Indicator: NY.GDP.MKTP.KD.ZG (GDP growth annual %)
        """
        # ISO code '1W' stands for World
        url = "https://api.worldbank.org/v2/country/1W/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2023"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1 and isinstance(data[1], list) and len(data[1]) > 0:
                    gdp_val = data[1][0].get("value")
                    if gdp_val is not None:
                        return self._create_response(
                            value=round(gdp_val, 2),
                            status="LIVE",
                            source="World Bank API",
                            source_url=url,
                            quality="LIVE",
                            update_freq="ANNUAL"
                        )
        except Exception:
            pass
            
        return self._fallback_response(3.0, "World Bank API")

    def get_interest_rate(self, country_code: str = "US") -> Dict[str, Any]:
        """
        Stub for getting interest rates. Can be expanded to fetch FRED data or RBI data.
        """
        return self._fallback_response(5.25, "Central Bank")
