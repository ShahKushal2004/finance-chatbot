from fastapi import APIRouter
from app.services import metrics
import pandas as pd

router = APIRouter()

@router.get("/by-category")
def by_category():
    return metrics.spending_by_category()

@router.get("/top-merchants")
def top_merchants(n: int = 5):
    return metrics.top_merchants(n=n)

@router.get("/monthly-totals")
def monthly():
    return metrics.monthly_totals()


@router.get("/top-expenses-week")
def top_expenses_week(k: int = 3):
    return metrics.latest_week_top_expenses(k=k)

@router.get("/daily-totals")
async def daily_totals():
    from app.services.data_store import get_transactions
    df = get_transactions()
    if df.empty:
        return []
    df["date"] = pd.to_datetime(df["date"]).dt.date # type: ignore
    summary = df.groupby("date")["amount"].sum().reset_index()
    return summary.to_dict(orient="records")

