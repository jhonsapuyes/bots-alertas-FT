

# strategy_engine/filters/base_filter.py

from abc import ABC, abstractmethod


class BaseFilter(ABC):

    @abstractmethod
    def apply(self, features: dict) -> dict:
        """
        Debe devolver:
        {
            "passed": bool,
            "reason": str | None,
            "meta": dict
        }
        """
        pass

