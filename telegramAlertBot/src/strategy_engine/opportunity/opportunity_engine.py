

# opportunity/opportunity_engine.py

from .detectors.trend_detector import TrendDetector
from .detectors.breakout_detector import BreakoutDetector
from .detectors.pullback_detector import PullbackDetector
from .detectors.range_detector import RangeDetector
from .detectors.liquidity_grab_detector import LiquidityGrabDetector
from .detectors.momentum_ignition_detector import MomentumIgnitionDetector
from .detectors.volatility_expansion_detector import VolatilityExpansionDetector
from .detectors.mean_reversion_detector import MeanReversionDetector
from .detectors.exhaustion_detector import ExhaustionDetector
from .detectors.reversal_detector import ReversalDetector
from .detectors.microRange_detector import MicroRangeDetector
from .detectors.continuationMicro_detector import ContinuationMicroDetector


class OpportunityEngine:

    def __init__(self):
        self.detectors = [
            TrendDetector(),
            BreakoutDetector(),
            PullbackDetector(),
            RangeDetector(),
            LiquidityGrabDetector(),
            MomentumIgnitionDetector(),
            VolatilityExpansionDetector(),
            MeanReversionDetector(),
            ExhaustionDetector(),
            ReversalDetector(),
            MicroRangeDetector(),
            ContinuationMicroDetector()
        ]

    def run(self, features, market):
        signals = []

        for detector in self.detectors:
            result = detector.detect(features, market)

            if result.get("detected"):
                signals.append({
                    "type": detector.name,
                    **result
                })

        return {
            "signals": signals,
            "count": len(signals),
            "best": max(signals, key=lambda x: x["confidence"], default=None)
        }

