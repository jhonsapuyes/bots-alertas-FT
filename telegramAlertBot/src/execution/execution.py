

# =========================================================
# EXECUTION ENGINE
# =========================================================

import time
import uuid


# =========================================================
# MAIN
# =========================================================

def execute_trade_plan(
    trade_plan,
    exchange="binance",
    symbol="ETHUSDT"
):

    # =====================================================
    # VALIDATION
    # =====================================================

    if not trade_plan["valid"]:

        return _blocked_execution_output(
            trade_plan=trade_plan,
            exchange=exchange,
            symbol=symbol
        )

    # =====================================================
    # TRADE DATA
    # =====================================================

    trade = trade_plan["trade"]

    side = trade["side"]

    entry = trade["entry"]
    stop_loss = trade["stop_loss"]
    take_profit = trade["take_profit"]

    position = trade["position"]

    execution = trade["execution"]

    # =====================================================
    # ENTRY
    # =====================================================

    entry_order_id = _generate_order_id()

    entry_order = {
        "id": entry_order_id,
        "status": "open",
        "side": _convert_side(side),
        "type": entry["type"],
        "price": entry["price"],
        "quantity": position["size"]
    }

    # =====================================================
    # STOP LOSS
    # =====================================================

    stop_order_id = _generate_order_id()

    stop_order = {
        "id": stop_order_id,
        "status": "pending",
        "type": "stop_market",
        "price": stop_loss["price"]
    }

    # =====================================================
    # TAKE PROFITS
    # =====================================================

    take_profit_orders = []

    tp_prices = [
        take_profit["tp1"],
        take_profit["tp2"],
        take_profit["tp3"]
    ]

    for tp_price in tp_prices:

        tp_order = {
            "id": _generate_order_id(),
            "price": tp_price,
            "status": "pending"
        }

        take_profit_orders.append(tp_order)

    # =====================================================
    # EXECUTION DETAILS
    # =====================================================

    execution_details = {
        "slippage": 0.02,
        "fees_estimated": _estimate_fees(
            entry_price=entry["price"],
            size=position["size"]
        ),
        "latency_ms": 43,
        "retry_count": 0,
        "partial_fill": False
    }

    # =====================================================
    # POSITION STATE
    # =====================================================

    position_state = {
        "position_opened": False,
        "entry_filled": False,
        "current_size": 0.0
    }

    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    return {

        # =================================================
        # STATUS
        # =================================================

        "success": True,

        "execution_state": "orders_placed",

        # =================================================
        # META
        # =================================================

        "meta": {
            "pipeline_stage": "EXECUTION_ENGINE",
            "exchange": exchange,
            "symbol": symbol,
            "timestamp": int(time.time())
        },

        # =================================================
        # ORDERS
        # =================================================

        "orders": {

            # ---------------------------------------------
            # ENTRY
            # ---------------------------------------------

            "entry_order": entry_order,

            # ---------------------------------------------
            # STOP LOSS
            # ---------------------------------------------

            "stop_order": stop_order,

            # ---------------------------------------------
            # TAKE PROFITS
            # ---------------------------------------------

            "take_profit_orders": take_profit_orders
        },

        # =================================================
        # EXECUTION DETAILS
        # =================================================

        "execution_details": execution_details,

        # =================================================
        # POSITION STATE
        # =================================================

        "position_state": position_state,

        # =================================================
        # ERRORS
        # =================================================

        "errors": []
    }


# =========================================================
# BLOCKED EXECUTION
# =========================================================

def _blocked_execution_output(
    trade_plan,
    exchange,
    symbol
):

    return {

        # =================================================
        # STATUS
        # =================================================

        "success": False,

        "execution_state": "blocked",

        # =================================================
        # META
        # =================================================

        "meta": {
            "pipeline_stage": "EXECUTION_ENGINE",
            "exchange": exchange,
            "symbol": symbol,
            "timestamp": int(time.time())
        },

        # =================================================
        # ORDERS
        # =================================================

        "orders": None,

        # =================================================
        # EXECUTION DETAILS
        # =================================================

        "execution_details": {
            "slippage": None,
            "fees_estimated": None,
            "latency_ms": 0,
            "retry_count": 0,
            "partial_fill": False
        },

        # =================================================
        # POSITION STATE
        # =================================================

        "position_state": {
            "position_opened": False,
            "entry_filled": False,
            "current_size": 0.0
        },

        # =================================================
        # ERRORS
        # =================================================

        "errors": trade_plan["reasons"]
    }


# =========================================================
# GENERATE ORDER ID
# =========================================================

def _generate_order_id():

    return str(uuid.uuid4().int)[:9]


# =========================================================
# SIDE CONVERTER
# =========================================================

def _convert_side(side):

    if side == "long":
        return "buy"

    if side == "short":
        return "sell"

    return "unknown"


# =========================================================
# FEES
# =========================================================

def _estimate_fees(
    entry_price,
    size
):

    fee_rate = 0.001

    return round(
        entry_price * size * fee_rate,
        2
    )

