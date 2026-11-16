import pandas as pd


# ==================================================
# SCORE HELPERS
# ==================================================

def calculate_savings_score(savings_rate):
    """
    Maximum: 25 points
    """

    savings_rate = float(savings_rate)

    if savings_rate >= 30:
        return 25
    elif savings_rate >= 20:
        return 20
    elif savings_rate >= 10:
        return 15
    elif savings_rate >= 5:
        return 8
    elif savings_rate > 0:
        return 3
    else:
        return 0


def calculate_expense_control_score(expense_ratio):
    """
    Maximum: 20 points

    expense_ratio = expenses / income * 100
    """

    expense_ratio = float(expense_ratio)

    if expense_ratio <= 50:
        return 20
    elif expense_ratio <= 60:
        return 18
    elif expense_ratio <= 70:
        return 15
    elif expense_ratio <= 80:
        return 10
    elif expense_ratio <= 100:
        return 5
    else:
        return 0


def calculate_budget_score(planned, actual):
    """
    Maximum: 20 points.

    Measures how closely actual spending
    stays within the planned budget.

    Each bucket contributes equally.
    """

    buckets = [
        "Needs",
        "Investment",
        "Lifestyle",
    ]

    bucket_scores = []

    for bucket in buckets:

        planned_amount = float(
            planned.get(bucket, 0)
        )

        actual_amount = float(
            actual.get(bucket, 0)
        )

        if planned_amount <= 0:

            if actual_amount <= 0:
                bucket_score = 100
            else:
                bucket_score = 0

        else:

            usage = (
                actual_amount
                / planned_amount
                * 100
            )

            if usage <= 90:
                bucket_score = 100
            elif usage <= 100:
                bucket_score = 90
            elif usage <= 110:
                bucket_score = 70
            elif usage <= 125:
                bucket_score = 40
            else:
                bucket_score = 0

        bucket_scores.append(
            bucket_score
        )

    average_score = (
        sum(bucket_scores)
        / len(bucket_scores)
    )

    return round(
        average_score
        / 100
        * 20
    )


def calculate_emergency_fund_score(
    available_savings,
    monthly_needs,
):
    """
    Maximum: 15 points.

    Emergency fund coverage is estimated as:

        available savings / monthly needs
    """

    available_savings = max(
        float(available_savings),
        0,
    )

    monthly_needs = max(
        float(monthly_needs),
        0,
    )

    if monthly_needs <= 0:

        if available_savings > 0:
            return 15

        return 0

    months_covered = (
        available_savings
        / monthly_needs
    )

    if months_covered >= 6:
        return 15
    elif months_covered >= 3:
        return 12
    elif months_covered >= 1:
        return 7
    elif months_covered > 0:
        return 3
    else:
        return 0


def calculate_goal_score(goals_df):
    """
    Maximum: 10 points.

    Uses average goal progress.
    """

    if goals_df is None:
        return 0

    if goals_df.empty:
        return 0

    data = goals_df.copy()

    data["Target Amount"] = pd.to_numeric(
        data.get("Target Amount", 0),
        errors="coerce",
    ).fillna(0)

    data["Current Saved"] = pd.to_numeric(
        data.get("Current Saved", 0),
        errors="coerce",
    ).fillna(0)

    valid = data[
        data["Target Amount"] > 0
    ].copy()

    if valid.empty:
        return 0

    valid["Progress"] = (
        valid["Current Saved"]
        / valid["Target Amount"]
    ).clip(
        lower=0,
        upper=1,
    )

    average_progress = (
        valid["Progress"].mean()
    )

    return round(
        average_progress * 10
    )


def calculate_investment_score(
    income,
    investment_amount,
):
    """
    Maximum: 10 points.

    This measures investment allocation,
    not investment performance.
    """

    income = float(income)
    investment_amount = max(
        float(investment_amount),
        0,
    )

    if income <= 0:
        return 0

    investment_rate = (
        investment_amount
        / income
        * 100
    )

    if investment_rate >= 20:
        return 10
    elif investment_rate >= 15:
        return 8
    elif investment_rate >= 10:
        return 6
    elif investment_rate >= 5:
        return 3
    elif investment_rate > 0:
        return 1
    else:
        return 0


# ==================================================
# OVERALL FINANCIAL HEALTH
# ==================================================

def calculate_financial_health(
    savings_rate,
    expense_ratio,
    planned,
    actual,
    available_savings,
    monthly_needs,
    goals_df,
    income,
    investment_amount,
):
    """
    Calculate complete Financial Health score.

    Total = 100 points.
    """

    savings_score = calculate_savings_score(
        savings_rate
    )

    expense_score = calculate_expense_control_score(
        expense_ratio
    )

    budget_score = calculate_budget_score(
        planned,
        actual,
    )

    emergency_score = calculate_emergency_fund_score(
        available_savings,
        monthly_needs,
    )

    goal_score = calculate_goal_score(
        goals_df
    )

    investment_score = calculate_investment_score(
        income,
        investment_amount,
    )

    total_score = (
        savings_score
        + expense_score
        + budget_score
        + emergency_score
        + goal_score
        + investment_score
    )

    total_score = max(
        0,
        min(
            100,
            total_score,
        ),
    )

    if total_score >= 85:
        status = "Excellent"

    elif total_score >= 70:
        status = "Healthy"

    elif total_score >= 50:
        status = "Moderate"

    elif total_score >= 30:
        status = "Needs Improvement"

    else:
        status = "Needs Attention"

    return {
        "total_score": int(total_score),
        "status": status,
        "savings_score": savings_score,
        "expense_score": expense_score,
        "budget_score": budget_score,
        "emergency_score": emergency_score,
        "goal_score": goal_score,
        "investment_score": investment_score,
    }


# ==================================================
# FINANCIAL INSIGHTS
# ==================================================

def generate_financial_insights(
    savings_rate,
    expense_ratio,
    emergency_months,
    goal_progress,
    investment_rate,
    budget_score,
):
    """
    Generate simple actionable insights.
    """

    strengths = []
    attention = []
    actions = []

    # ----------------------------------------------
    # Savings
    # ----------------------------------------------

    if savings_rate >= 20:

        strengths.append(
            "Your savings rate is healthy."
        )

    elif savings_rate >= 10:

        attention.append(
            "Your savings rate is moderate."
        )

        actions.append(
            "Try gradually increasing your savings rate."
        )

    else:

        attention.append(
            "Your savings rate is low."
        )

        actions.append(
            "Review your spending and try to increase the amount you save each month."
        )

    # ----------------------------------------------
    # Expense ratio
    # ----------------------------------------------

    if expense_ratio <= 70:

        strengths.append(
            "Your spending is within a reasonable range of your income."
        )

    elif expense_ratio <= 100:

        attention.append(
            "A large portion of your income is being spent."
        )

        actions.append(
            "Review recurring and lifestyle expenses."
        )

    else:

        attention.append(
            "Your expenses are higher than your income."
        )

        actions.append(
            "Prioritize reducing expenses or increasing income."
        )

    # ----------------------------------------------
    # Emergency fund
    # ----------------------------------------------

    if emergency_months >= 6:

        strengths.append(
            "Your estimated emergency fund coverage is strong."
        )

    elif emergency_months >= 3:

        strengths.append(
            "You have a reasonable emergency fund base."
        )

    else:

        attention.append(
            "Your emergency fund coverage is below 3 months."
        )

        actions.append(
            "Build an emergency fund toward at least 3 months of essential expenses."
        )

    # ----------------------------------------------
    # Goals
    # ----------------------------------------------

    if goal_progress >= 0.5:

        strengths.append(
            "Your financial goals are making good progress."
        )

    elif goal_progress > 0:

        attention.append(
            "Your financial goals are progressing slowly."
        )

        actions.append(
            "Consider making regular contributions toward your goals."
        )

    else:

        attention.append(
            "You currently have little or no progress toward your financial goals."
        )

        actions.append(
            "Create or start contributing to a financial goal."
        )

    # ----------------------------------------------
    # Investments
    # ----------------------------------------------

    if investment_rate >= 10:

        strengths.append(
            "You are allocating part of your income toward investments."
        )

    else:

        attention.append(
            "Your investment allocation is relatively low."
        )

        actions.append(
            "Consider allocating a suitable portion of your savings toward long-term investments."
        )

    # ----------------------------------------------
    # Budget
    # ----------------------------------------------

    if budget_score >= 16:

        strengths.append(
            "Your spending is generally aligned with your budget."
        )

    elif budget_score >= 10:

        attention.append(
            "Some spending categories are moving away from your planned budget."
        )

        actions.append(
            "Review categories that regularly exceed their planned amounts."
        )

    else:

        attention.append(
            "Your actual spending is significantly different from your planned budget."
        )

        actions.append(
            "Review your Planning settings and adjust spending where necessary."
        )

    return {
        "strengths": strengths,
        "attention": attention,
        "actions": actions,
    }
