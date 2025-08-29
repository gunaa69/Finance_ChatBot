# finance_utils.py
from typing import Dict, List, Tuple
import math

def generate_budget_summary(expenses: Dict[str, float]) -> Tuple[str, float]:
    total = float(sum(expenses.values()))
    lines = [f"- {k}: ₹{v:.2f}" for k, v in expenses.items()]
    summary = f"💰 Total monthly spending: **₹{total:.2f}**\n\nBreakdown:\n" + "\n".join(lines)
    return summary, total

def spending_insights(expenses: Dict[str, float]) -> List[str]:
    total = sum(expenses.values()) or 1.0
    insights = []
    # ratio based checks
    entertainment_ratio = expenses.get("Entertainment", 0) / total
    groceries_ratio = expenses.get("Groceries", 0) / total
    rent_ratio = expenses.get("Rent", 0) / total

    if entertainment_ratio > 0.12:
        insights.append("⚠️ Entertainment spending is relatively high (>12% of total). Consider cutting subscriptions or nights out.")
    if groceries_ratio < 0.12:
        insights.append("🍎 Groceries low relative to spending — ensure you're not under-eating or missing essentials.")
    if rent_ratio > 0.4:
        insights.append("🏠 Rent is >40% of income – if possible look for alternatives or negotiate rent.")
    if expenses.get("Investments", 0) < 0.1 * total:
        insights.append("📈 Investments are less than 10% of spending — consider increasing to build long-term wealth.")
    if not insights:
        insights.append("✅ Your spending looks fairly balanced for a default profile. Keep tracking it!")

    # tactical tips
    insights.append("Tip: Automate at least 20% of savings to a separate account each month for consistency.")
    return insights

def simple_tax_estimator(annual_income: float, deductions: float = 0.0) -> Dict[str, float]:
    """
    Very simple progressive slab estimator (example), not a replacement for real tax advice.
    Uses example progressive slabs (replace with local tax system).
    """
    taxable = max(0.0, annual_income - deductions)
    # Example simplified slabs (illustrative only)
    slabs = [(250000, 0.0), (250000, 0.05), (500000, 0.2), (float("inf"), 0.3)]
    remaining = taxable
    tax = 0.0
    prev = 0.0
    for slab_amount, rate in slabs:
        amount = min(remaining, slab_amount - prev if slab_amount != float("inf") else remaining)
        if amount <= 0:
            prev = slab_amount
            continue
        tax += amount * rate
        remaining -= amount
        prev = slab_amount
        if remaining <= 0:
            break
    # quick cess
    cess = tax * 0.04
    total_tax = tax + cess
    return {"taxable_income": taxable, "tax_before_cess": tax, "cess_4pct": cess, "total_tax": total_tax}

def investment_suggestions(profile: str, monthly_surplus: float) -> List[str]:
    """
    Return simple recommended instruments.
    profile: "Student" or "Professional"
    """
    suggestions = []
    if monthly_surplus <= 0:
        suggestions.append("You have no surplus—prioritize creating a small emergency buffer first (₹1000+).")
        return suggestions

    months = 12
    annual_surplus = monthly_surplus * months

    if profile == "Student":
        suggestions.append("1) Start a small SIP in an ETF/Index fund — low cost, long term.")
        if monthly_surplus >= 50:
            suggestions.append("2) Consider a recurring deposit or a small emergency fund for 3 months of expenses.")
    else:
        # Professional
        suggestions.append("1) Maximize tax-advantaged accounts (e.g., 80C/401k/retirement) up to limits.")
        if monthly_surplus >= 200:
            suggestions.append("2) Allocate: 40% equities (ETFs), 30% debt (bond funds/FDs), 20% tax-saving, 10% cash buffer.")
        else:
            suggestions.append("2) If surplus is small, prioritize emergency fund (3-6 months), then start SIP.")

    suggestions.append(f"Estimated annual investable amount: ₹{annual_surplus:.2f}")
    return suggestions
