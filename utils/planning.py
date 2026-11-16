import pandas as pd


VALID_BUCKETS = [
    "Needs",
    "Investment",
    "Lifestyle",
]


def classify_expenses(
    expense_df,
    category_mapping,
):
    """
    Apply user-defined planning bucket mapping
    to expense transactions.

    Unknown categories are placed into Needs
    temporarily so that expenses are not ignored.
    """

    result = expense_df.copy()

    if result.empty:
        result["Planning Bucket"] = pd.Series(
            dtype="object"
        )
        return result

    mapping = {
        str(category).strip(): str(bucket).strip()
        for category, bucket in category_mapping.items()
        if str(category).strip()
        and str(bucket).strip() in VALID_BUCKETS
    }

    result["Planning Bucket"] = (
        result["Category"]
        .fillna("")
        .astype(str)
        .str.strip()
        .map(mapping)
        .fillna("Needs")
    )

    return result


def calculate_budget_actuals(
    expense_df,
    category_mapping,
):
    """
    Calculate actual spending for each
    planning bucket.
    """

    classified_df = classify_expenses(
        expense_df,
        category_mapping,
    )

    actual_needs = classified_df.loc[
        classified_df["Planning Bucket"] == "Needs",
        "Expense Amount",
    ].sum()

    actual_investment = classified_df.loc[
        classified_df["Planning Bucket"] == "Investment",
        "Expense Amount",
    ].sum()

    actual_lifestyle = classified_df.loc[
        classified_df["Planning Bucket"] == "Lifestyle",
        "Expense Amount",
    ].sum()

    return {
        "Needs": float(actual_needs),
        "Investment": float(actual_investment),
        "Lifestyle": float(actual_lifestyle),
    }


def calculate_planned_amounts(
    income,
    needs_percent,
    investment_percent,
    lifestyle_percent,
):
    """
    Convert budget percentages into
    planned rupee amounts.
    """

    return {
        "Needs": (
            income
            * needs_percent
            / 100
        ),
        "Investment": (
            income
            * investment_percent
            / 100
        ),
        "Lifestyle": (
            income
            * lifestyle_percent
            / 100
        ),
    }


def budget_comparison(
    planned,
    actual,
):
    """
    Compare planned and actual spending.
    Positive difference means amount remaining.
    Negative difference means over budget.
    """

    rows = []

    for bucket in VALID_BUCKETS:

        planned_amount = float(
            planned.get(bucket, 0)
        )

        actual_amount = float(
            actual.get(bucket, 0)
        )

        difference = (
            planned_amount
            - actual_amount
        )

        rows.append(
            {
                "Category": bucket,
                "Planned": planned_amount,
                "Actual": actual_amount,
                "Difference": difference,
            }
        )

    return pd.DataFrame(rows)
