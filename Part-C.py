# ============================================================
#  Day-08 | PART B — Stretch Problem
#  Indian Income Tax Calculator (New Regime, FY 2024-25)
#  Progressive slab-wise taxation with detailed breakdown
# ============================================================

# ── Tax slabs: (lower_bound, upper_bound, rate_percent) ──────
# Upper bound of None means "no ceiling" (above 15L slab)

TAX_SLABS = [
    (0,          300_000,  0),
    (300_000,    700_000,  5),
    (700_000,  1_000_000, 10),
    (1_000_000, 1_200_000, 15),
    (1_200_000, 1_500_000, 20),
    (1_500_000,      None, 30),
]

STANDARD_DEDUCTION = 75_000   # FY 2024-25 new regime
REBATE_87A_LIMIT   = 700_000  # No tax if taxable income ≤ 7L (after std deduction)
REBATE_87A_MAX     = 25_000   # Max rebate amount


# ── helpers ──────────────────────────────────────────────────

def format_inr(amount: float) -> str:
    """Format a number as Indian Rupees with ₹ symbol and commas."""
    # Indian numbering: last 3 digits, then groups of 2
    amount = round(amount, 2)
    is_negative = amount < 0
    amount = abs(amount)
    integer_part = int(amount)
    decimal_part = round(amount - integer_part, 2)

    s = str(integer_part)
    if len(s) > 3:
        last_three = s[-3:]
        rest = s[:-3]
        grouped = ""
        for i, ch in enumerate(reversed(rest)):
            if i > 0 and i % 2 == 0:
                grouped = "," + grouped
            grouped = ch + grouped
        s = grouped + "," + last_three
    
    decimal_str = f"{decimal_part:.2f}"[1:]   # ".xx"
    result = f"₹{s}{decimal_str}"
    return f"-{result}" if is_negative else result


def get_income(prompt: str) -> float:
    """Validate and return a non-negative annual income."""
    while True:
        raw = input(prompt).strip().replace(",", "").replace("₹", "")
        try:
            value = float(raw)
        except ValueError:
            print("  ✗ Invalid input. Please enter a numeric value.")
            continue
        if value < 0:
            print("  ✗ Income cannot be negative.")
            continue
        return value


# ── core engine ───────────────────────────────────────────────

def compute_tax(taxable_income: float) -> tuple[list[dict], float]:
    """
    Apply progressive slab taxation.
    Returns (slab_details_list, total_tax_before_rebate).
    """
    slab_details = []
    remaining    = taxable_income
    total_tax    = 0.0

    for lower, upper, rate in TAX_SLABS:
        if remaining <= 0:
            break

        # Width of this slab
        slab_width  = (upper - lower) if upper is not None else float("inf")
        # Income that falls in this slab
        income_in_slab = min(remaining, slab_width)
        tax_in_slab    = income_in_slab * rate / 100

        slab_details.append({
            "range":         f"{format_inr(lower)} – " + (format_inr(upper) if upper else "Above"),
            "rate":          rate,
            "income_in_slab": income_in_slab,
            "tax":           tax_in_slab,
        })

        total_tax += tax_in_slab
        remaining -= income_in_slab

    return slab_details, total_tax


def calculate_and_display(gross_income: float) -> None:
    """Full calculation pipeline + formatted output."""

    # ── Step 1: Standard deduction ───────────────────────────
    std_deduction   = min(STANDARD_DEDUCTION, gross_income)
    taxable_income  = max(0.0, gross_income - std_deduction)

    # ── Step 2: Slab-wise tax ────────────────────────────────
    slab_details, tax_before_rebate = compute_tax(taxable_income)

    # ── Step 3: Section 87A rebate ───────────────────────────
    rebate = 0.0
    if taxable_income <= REBATE_87A_LIMIT:
        rebate = min(tax_before_rebate, REBATE_87A_MAX)

    tax_after_rebate = tax_before_rebate - rebate

    # ── Step 4: Health & Education Cess (4%) ─────────────────
    cess = tax_after_rebate * 0.04
    total_tax_payable = tax_after_rebate + cess

    # ── Step 5: Effective rate on GROSS income ────────────────
    effective_rate = (total_tax_payable / gross_income * 100) if gross_income > 0 else 0.0

    # ════════════════════════════════════════════════════════
    #  OUTPUT
    # ════════════════════════════════════════════════════════
    W = 62   # table width
    print("\n" + "═" * W)
    print("  INCOME TAX CALCULATOR — New Regime, FY 2024-25".center(W))
    print("═" * W)

    # Income summary
    print(f"\n  {'Gross Annual Income':<32} {format_inr(gross_income):>16}")
    print(f"  {'Less: Standard Deduction':<32} {('-' + format_inr(std_deduction)):>16}")
    print(f"  {'─'*48}")
    print(f"  {'Taxable Income':<32} {format_inr(taxable_income):>16}")

    # Slab breakdown
    print(f"\n  {'─'*W}")
    print(f"  {'SLAB-WISE BREAKDOWN':^{W-4}}")
    print(f"  {'─'*W}")
    header = f"  {'Slab Range':<22} {'Rate':>6}  {'Income in Slab':>16}  {'Tax':>12}"
    print(header)
    print(f"  {'─'*W}")

    for s in slab_details:
        if s["income_in_slab"] == 0:
            continue
        label = f"  {s['range']:<22} {str(s['rate'])+'%':>6}  "
        nums  = f"{format_inr(s['income_in_slab']):>16}  {format_inr(s['tax']):>12}"
        print(label + nums)

    print(f"  {'─'*W}")
    print(f"  {'Tax Before Rebate':<46} {format_inr(tax_before_rebate):>12}")

    # Rebate
    if rebate > 0:
        print(f"  {'Less: Rebate u/s 87A':<46} {('-' + format_inr(rebate)):>12}")
        print(f"  {'Tax After Rebate':<46} {format_inr(tax_after_rebate):>12}")

    # Cess
    print(f"  {'Add: Health & Education Cess @ 4%':<46} {format_inr(cess):>12}")
    print(f"  {'═'*W}")
    print(f"  {'TOTAL TAX PAYABLE':<46} {format_inr(total_tax_payable):>12}")
    print(f"  {'═'*W}")

    # Summary stats
    print(f"\n  {'Effective Tax Rate (on Gross Income)':<44} {effective_rate:>6.2f}%")
    print(f"  {'In-Hand Annual Income':<44} {format_inr(gross_income - total_tax_payable):>14}")
    print(f"  {'In-Hand Monthly Income':<44} {format_inr((gross_income - total_tax_payable)/12):>14}")
    print("═" * W + "\n")

    # ── Verdict ──────────────────────────────────────────────
    if total_tax_payable == 0:
        verdict = "✓ No tax liability — fully covered by rebate u/s 87A or nil slab."
    elif effective_rate < 10:
        verdict = f"✓ Low tax burden at {effective_rate:.2f}% effective rate."
    elif effective_rate < 20:
        verdict = f"◈ Moderate tax burden at {effective_rate:.2f}% effective rate."
    else:
        verdict = f"◆ High tax bracket — consider consulting a tax advisor."

    print(f"  {verdict}\n")


# ── entry point ───────────────────────────────────────────────

def main() -> None:
    print("=" * 62)
    print("  Indian Income Tax Calculator (New Regime — FY 2024-25)")
    print("=" * 62)
    print("  Enter your annual income below.")
    print("  (You may type amounts like 1200000 or 12,00,000)\n")

    gross_income = get_income("  Annual Gross Income (₹): ")
    calculate_and_display(gross_income)


if __name__ == "__main__":
    main()
