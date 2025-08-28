import pandas as pd
from typing import Optional

# In-memory DataFrame
_df: Optional[pd.DataFrame] = None

REQUIRED_COLUMNS = ["date", "description", "amount", "category"]

def reset():
    global _df
    _df = None

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d.columns = [c.strip().lower() for c in d.columns]
    if "date" in d.columns:
        d["date"] = pd.to_datetime(d["date"],dayfirst=True, errors="coerce")
    if "amount" in d.columns:
        d["amount"] = pd.to_numeric(d["amount"], errors="coerce")
    return d

def save_transactions(df: pd.DataFrame) -> int:
    """Replace in-memory store with uploaded data (normalized)."""
    global _df
    d = _normalize_columns(df)
    missing = set(REQUIRED_COLUMNS) - set(d.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    # Drop rows with bad date/amount
    d = d.dropna(subset=["date", "amount"])
    _df = d.reset_index(drop=True)
    return len(_df)

def get_transactions() -> pd.DataFrame:
    global _df
    if _df is None:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)
    return _df
