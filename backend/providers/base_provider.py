from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class BaseProvider(ABC):
    def __init__(self):
        # We can load API keys here using os.getenv
        pass
        
    def _create_response(self, value: Any, status: str, source: str, source_url: str = "", quality: str = "LIVE", update_freq: str = "near_real_time") -> Dict[str, Any]:
        return {
            "value": value,
            "source": source,
            "source_url": source_url,
            "retrieved_at": datetime.utcnow().isoformat(),
            "data_timestamp": datetime.utcnow().isoformat(),
            "update_frequency": update_freq,
            "data_quality": quality,
            "status": status
        }

    def _fallback_response(self, default_value: Any, source: str) -> Dict[str, Any]:
        return {
            "value": default_value,
            "source": f"{source} (Fallback)",
            "source_url": "local_db",
            "retrieved_at": datetime.utcnow().isoformat(),
            "data_timestamp": datetime.utcnow().isoformat(),
            "update_frequency": "STATIC",
            "data_quality": "FALLBACK",
            "status": "UNAVAILABLE_USING_FALLBACK"
        }
