import pandas as pd
from typing import Dict, Any
from app.services.data_store import get_transactions # type: ignore


def _safe_df() -> pd.DataFrame:
    df = get_transactions()
    if df.empty:
        return df
    # ensure date column is datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])  # drop rows with invalid dates
    
    # treat negative amounts as refunds and exclude from spend
    df = df[df["amount"] > 0].copy()
    return df


def spending_by_category() -> Dict[str, float]:
    df = _safe_df()
    if df.empty:
        return {}
    return (df.groupby("category")["amount"]
              .sum()
              .sort_values(ascending=False)
              .round(2)
              .to_dict())

def top_merchants(n: int = 3) -> Dict[str, float]:
    df = _safe_df()
    if df.empty:
        return {}
    # treat "description" as merchant
    return (df.groupby("description")["amount"]
              .sum()
              .sort_values(ascending=False)
              .head(n)
              .round(2)
              .to_dict())

def monthly_totals() -> Dict[str, float]:
    df = _safe_df()
    if df.empty:
        return {}
    s = (df
         .assign(month=df["date"].dt.to_period("M").astype(str))
         .groupby("month")["amount"]
         .sum()
         .sort_index()
         .round(2))
    return s.to_dict()

def fastest_growing_category() -> Dict[str, Any]:
    """
    Very small MoM growth heuristic:
    - Compute month totals per category
    - Compute MoM pct change for each category
    - Return the category with highest last available pct change
    """
    df = _safe_df()
    if df.empty:
        return {}

    g = (df.assign(month=df["date"].dt.to_period("M").astype(str))
            .groupby(["category", "month"])["amount"]
            .sum()
            .reset_index())

    # pivot to months across columns, fill 0, then pct change across months
    pivot = g.pivot(index="category", columns="month", values="amount").fillna(0).sort_index(axis=1)
    if pivot.shape[1] < 2:
        return {}

    pct = pivot.pct_change(axis=1).replace([pd.NA, pd.NaT, float("inf"), -float("inf")], 0).fillna(0)
    last_col = pct.columns[-1]
    last_growth = pct[last_col].sort_values(ascending=False)

    top_cat = last_growth.index[0]
    return {
        "month": last_col,
        "category": top_cat,
        "growth_pct": round(float(last_growth.iloc[0]) * 100, 2)
    }

def latest_week_top_expenses(k: int = 3) -> Dict[str, float]:
    df = _safe_df()
    if df.empty:
        return {}
    last_date = df["date"].max()
    week_start = last_date - pd.Timedelta(days=6)
    w = df[(df["date"] >= week_start) & (df["date"] <= last_date)].copy()
    if w.empty:
        return {}
    # biggest line items (not aggregated)
    top = w.sort_values("amount", ascending=False).head(k)
    # use description as key with amount
    return {f'{row["description"]} ({row["date"].date()})': round(float(row["amount"]), 2)
            for _, row in top.iterrows()}
