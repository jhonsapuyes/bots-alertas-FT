

def opportunityDetect_exhaustion(ctx):

    fatigue = ctx.get("fatigue", {})
    d = ctx.get("data", {})

    if not fatigue:
        return None

    phase = fatigue.get("phase")
    score = fatigue.get("score", 0)

    if phase != "exhaustion":
        return None

    # 🧠 agotamiento confirmado
    if score <= -3:
        return {
            "buy": False,
            "sell": False,
            "strength": "exit",
            "reason": "trend exhaustion",
            "score": score
        }

    return None

