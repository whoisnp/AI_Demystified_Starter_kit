from typing import Optional

def estimate_budget(days: int, budget: Optional[str]) -> str:
    print(f"🛠️ [TOOL: budget] Estimating budget for {days} days...")
    if budget:
        print(f"🛠️ [TOOL: budget] User provided budget constraints: {budget}")
        return f"Trip planned within {budget}"
    else:
        total = days * 2000
        print(f"🛠️ [TOOL: budget] Calculating mock total: ₹{total}")
        return f"Estimated budget: ₹{total} for {days} days"
