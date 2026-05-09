# =========================================================
# PROTECTION / SAFETY LAYER
# =========================================================

import time


# =========================================================
# MAIN
# =========================================================

def protect_execution(
    execution_data
):

    # =====================================================
    # VALIDATION
    # =====================================================

    if not execution_data["success"]:

        return _blocked_protection_output(
            execution_data
        )

    # =====================================================
    # INPUTS
    # =====================================================

    execution_state = execution_data["execution_state"]

    meta = execution_data["meta"]

    orders = execution_data["orders"]

    execution_details = execution_data[
        "execution_details"
    ]

    position_state = execution_data[
        "position_state"
    ]

    # =====================================================
    # ENTRY ORDER
    # =====================================================

    entry_order = orders["entry_order"]

    entry_order_status = entry_order["status"]

    # =====================================================
    # STOP ORDER
    # =====================================================

    stop_order = orders["stop_order"]

    stop_order_exists = (
        stop_order is not None
    )

    # =====================================================
    # TAKE PROFITS
    # =====================================================

    take_profit_orders = orders[
        "take_profit_orders"
    ]

    tp_count = len(take_profit_orders)

    # =====================================================
    # SAFETY CHECKS
    # =====================================================

    safety_checks = {

        # -------------------------------------------------
        # STOP LOSS
        # -------------------------------------------------

        "stop_loss_protected": (
            stop_order_exists
        ),

        # -------------------------------------------------
        # TAKE PROFITS
        # -------------------------------------------------

        "take_profit_protected": (
            tp_count >= 1
        ),

        # -------------------------------------------------
        # EXECUTION HEALTH
        # -------------------------------------------------

        "execution_latency_safe": (
            execution_details["latency_ms"]
            < 200
        ),

        # -------------------------------------------------
        # SLIPPAGE
        # -------------------------------------------------

        "slippage_safe": (
            execution_details["slippage"]
            <= 0.10
        ),

        # -------------------------------------------------
        # POSITION
        # -------------------------------------------------

        "position_size_valid": (
            entry_order["quantity"] > 0
        )
    }

    # =====================================================
    # SAFETY SCORE
    # =====================================================

    passed_checks = sum(
        safety_checks.values()
    )

    total_checks = len(safety_checks)

    safety_score = round(
        passed_checks / total_checks,
        2
    )

    # =====================================================
    # OVERALL STATUS
    # =====================================================

    fully_protected = (
        safety_score >= 0.80
    )

    protection_state = (
        "protected"
        if fully_protected
        else "risk_detected"
    )

    # =====================================================
    # WARNINGS
    # =====================================================

    warnings = []

    if not safety_checks[
        "stop_loss_protected"
    ]:
        warnings.append(
            "missing stop loss protection"
        )

    if not safety_checks[
        "take_profit_protected"
    ]:
        warnings.append(
            "missing take profit protection"
        )

    if not safety_checks[
        "execution_latency_safe"
    ]:
        warnings.append(
            "high execution latency"
        )

    if not safety_checks[
        "slippage_safe"
    ]:
        warnings.append(
            "high slippage detected"
        )

    if not safety_checks[
        "position_size_valid"
    ]:
        warnings.append(
            "invalid position size"
        )

    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    return {

        # =================================================
        # STATUS
        # =================================================

        "success": fully_protected,

        "protection_state": protection_state,

        # =================================================
        # META
        # =================================================

        "meta": {
            "pipeline_stage": (
                "PROTECTION_LAYER"
            ),
            "exchange": meta["exchange"],
            "symbol": meta["symbol"],
            "timestamp": int(time.time())
        },

        # =================================================
        # SAFETY CHECKS
        # =================================================

        "safety_checks": safety_checks,

        # =================================================
        # SAFETY SCORE
        # =================================================

        "safety_metrics": {
            "score": safety_score,
            "checks_passed": passed_checks,
            "total_checks": total_checks
        },

        # =================================================
        # ORDER STATUS
        # =================================================

        "order_status": {
            "entry_order_status": (
                entry_order_status
            ),
            "stop_order_active": (
                stop_order_exists
            ),
            "tp_orders_active": tp_count
        },

        # =================================================
        # POSITION STATE
        # =================================================

        "position_state": position_state,

        # =================================================
        # WARNINGS
        # =================================================

        "warnings": warnings
    }


# =========================================================
# BLOCKED OUTPUT
# =========================================================

def _blocked_protection_output(
    execution_data
):

    meta = execution_data["meta"]

    return {

        # =================================================
        # STATUS
        # =================================================

        "success": False,

        "protection_state": "blocked",

        # =================================================
        # META
        # =================================================

        "meta": {
            "pipeline_stage": (
                "PROTECTION_LAYER"
            ),
            "exchange": meta["exchange"],
            "symbol": meta["symbol"],
            "timestamp": int(time.time())
        },

        # =================================================
        # SAFETY CHECKS
        # =================================================

        "safety_checks": None,

        # =================================================
        # SAFETY METRICS
        # =================================================

        "safety_metrics": {
            "score": 0.0,
            "checks_passed": 0,
            "total_checks": 0
        },

        # =================================================
        # ORDER STATUS
        # =================================================

        "order_status": None,

        # =================================================
        # POSITION STATE
        # =================================================

        "position_state": {
            "position_opened": False,
            "entry_filled": False,
            "current_size": 0.0
        },

        # =================================================
        # WARNINGS
        # =================================================

        "warnings": execution_data["errors"]
    }