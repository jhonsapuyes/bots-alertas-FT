

# opportunity/base_detector.py

from abc import ABC, abstractmethod


class BaseDetector(ABC):
    """
    Contrato base para TODOS los detectores de oportunidades.
    """

    name = "base_detector"

    @abstractmethod
    def detect(self, features: dict, market: dict) -> dict:
        """
        Retorna:
        {
            "detected": bool,
            "confidence": float (0-1),
            "side": "long" | "short" | None,
            "reason": str
        }
        """
        pass

    def _safe(self, value, default=None):
        return value if value is not None else default
    
