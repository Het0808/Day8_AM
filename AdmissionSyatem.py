# ============================================================
#  Day-08 | TAKE-HOME ASSIGNMENT
#  Student Admission Decision System
#  Topics: if/elif/else, comparison ops, logical ops,
#          nested if, ternary operator, match-case, input validation
# ============================================================


# ── helpers ──────────────────────────────────────────────────

def get_float(prompt: str, lo: float, hi: float) -> float:
    """Validate and return a float within [lo, hi]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print(f"  ✗ Invalid input. Please enter a number between {lo} and {hi}.")
            continue
        if not (lo <= value <= hi):
            print(f"  ✗ Out of range. Must be between {lo} and {hi}.")
            continue
        return value


def get_yes_no(prompt: str) -> bool:
    """Validate and return True for 'yes', False for 'no'."""
    while True:
        raw = input(prompt).strip().lower()
        if raw in ("yes", "y"):
            return True
        elif raw in ("no", "n"):
            return False
        else:
            print("  ✗ Please enter 'yes' or 'no'.")


def get_category(prompt: str) -> str:
    """Validate and return a recognised category string."""
    valid = {"general", "obc", "sc_st"}
    while True:
        raw = input(prompt).strip().lower()
        if raw in valid:
            return raw
        print(f"  ✗ Invalid category. Choose from: general / obc / sc_st")


# ── cutoffs ──────────────────────────────────────────────────

CATEGORY_CUTOFF = {
    "general": 75,
    "obc":     65,
    "sc_st":   55,
}

MIN_GPA        = 7.0
SCHOLARSHIP_SCORE = 95


# ── core logic ───────────────────────────────────────────────

def evaluate_admission(entrance_score: float,
                       gpa: float,
                       has_recommendation: bool,
                       category: str,
                       extracurricular_score: float) -> None:

    print("\n" + "─" * 50)

    # ── Rule 4: auto-admit with scholarship ──────────────────
    if entrance_score >= SCHOLARSHIP_SCORE:
        print("Result:\nADMITTED (Scholarship)")
        print(f"Reason: Entrance score {entrance_score:.0f} ≥ {SCHOLARSHIP_SCORE} — "
              "auto-admitted with full scholarship.")
        return

    # ── Bonus calculation ────────────────────────────────────
    bonus       = 0
    bonus_parts = []

    if has_recommendation:
        bonus += 5
        bonus_parts.append("+5 (recommendation)")

    if extracurricular_score > 8:
        bonus += 3
        bonus_parts.append("+3 (extracurricular)")

    effective_score = entrance_score + bonus

    # Print bonus info (ternary operator used for the label)
    bonus_line = (f"Bonus Applied: {' '.join(bonus_parts)}"
                  if bonus_parts else "Bonus Applied: None")
    print(bonus_line)
    print(f"Effective Score: {effective_score:.0f}")

    # ── Determine cutoff using match-case ────────────────────
    match category:
        case "general":
            cutoff      = CATEGORY_CUTOFF["general"]
            cat_display = "General"
        case "obc":
            cutoff      = CATEGORY_CUTOFF["obc"]
            cat_display = "OBC"
        case "sc_st":
            cutoff      = CATEGORY_CUTOFF["sc_st"]
            cat_display = "SC/ST"
        case _:
            # Should never reach here due to validated input
            print("REJECTED\nReason: Unknown category.")
            return

    # ── Decision tree ────────────────────────────────────────
    score_ok = effective_score >= cutoff
    gpa_ok   = gpa >= MIN_GPA

    if score_ok and gpa_ok:
        print("\nResult:\nADMITTED (Regular)")
        print(f"Reason: Meets {cat_display} cutoff "
              f"({effective_score:.0f} ≥ {cutoff}) "
              f"and GPA requirement ({gpa:.1f} ≥ {MIN_GPA}).")

    elif score_ok and not gpa_ok:
        print("\nResult:\nREJECTED")
        print(f"Reason: GPA too low ({gpa:.1f} < {MIN_GPA} required).")

    elif not score_ok and gpa_ok:
        # Close miss → waitlist
        gap = cutoff - effective_score
        if gap <= 5:
            print("\nResult:\nWAITLISTED")
            print(f"Reason: Effective score {effective_score:.0f} is {gap:.0f} point(s) "
                  f"below {cat_display} cutoff ({cutoff}). GPA is satisfactory.")
        else:
            print("\nResult:\nREJECTED")
            print(f"Reason: Effective score {effective_score:.0f} does not meet "
                  f"{cat_display} cutoff ({cutoff}).")

    else:  # both fail
        print("\nResult:\nREJECTED")
        print(f"Reason: Effective score {effective_score:.0f} does not meet "
              f"{cat_display} cutoff ({cutoff}), "
              f"and GPA ({gpa:.1f}) is below minimum ({MIN_GPA}).")


# ── entry point ───────────────────────────────────────────────

def main() -> None:
    print("=" * 50)
    print("  University Admission Decision System")
    print("=" * 50)

    entrance_score       = get_float("Entrance Score (0–100): ",  0, 100)
    gpa                  = get_float("GPA (0.0–10.0): ",          0,  10)
    has_recommendation   = get_yes_no("Recommendation Letter? (yes/no): ")
    category             = get_category("Category (general / obc / sc_st): ")
    extracurricular_score = get_float("Extracurricular Score (0–10): ", 0, 10)

    evaluate_admission(
        entrance_score,
        gpa,
        has_recommendation,
        category,
        extracurricular_score,
    )
    print("─" * 50)


if __name__ == "__main__":
    main()
