import os
import requests
from typing import Dict, Any
from .base_provider import BaseProvider

class WeatherProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        
    def get_route_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Uses Open-Meteo (Free, NO API Key required, Public API) for real-time weather.
        """
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current = data.get("current_weather", {})
                
                wind_speed = current.get("windspeed", 0)
                # Calculate simple weather risk index based on wind speed
                risk_index = min(100, (wind_speed / 50) * 100)
                
                return self._create_response(
                    value=risk_index,
                    status="LIVE",
                    source="Open-Meteo",
                    source_url=url,
                    quality="LIVE",
                    update_freq="near_real_time"
                )
        except Exception:
            pass
            
        return self._fallback_response(50, "Open-Meteo")

