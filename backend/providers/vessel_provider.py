import os
import requests
from typing import Dict, Any, List
from .base_provider import BaseProvider

class VesselProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("VESSELFINDER_API_KEY")

    def get_available_vessels(self, port: str, vessel_class: str) -> Dict[str, Any]:
        """
        Fetches available vessels near a port. 
        Will use live API if key is present, else falls back to hybrid approach logic.
        """
        if self.api_key:
            # Example VesselFinder endpoint implementation
            url = f"https://api.vesselfinder.com/vessels?port={port}&type={vessel_class}&userkey={self.api_key}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return self._create_response(
                        value=response.json(),
                        status="LIVE",
                        source="VesselFinder",
                        source_url=url
                    )
            except Exception:
                pass
                
        # If API key missing or request fails, we must notify we don't have live real-time access
        # But we won't invent data. We will return "UNAVAILABLE".
        return {
            "value": [],
            "source": "VesselFinder",
            "source_url": "https://api.vesselfinder.com",
            "retrieved_at": self._create_response(0,"","")["retrieved_at"],
            "data_timestamp": self._create_response(0,"","")["retrieved_at"],
            "update_frequency": "near_real_time",
            "data_quality": "REQUIRES_API_KEY",
            "status": "UNAVAILABLE"
        }
