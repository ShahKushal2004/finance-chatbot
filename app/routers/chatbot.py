from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services import metrics
from app.services.llm import ask_llm
import json

router = APIRouter()

@router.post("/")
def chatbot(req: ChatRequest):
    # Build transaction summaries
    context = {
        "spending_by_category": metrics.spending_by_category(),
        "top_merchants": metrics.top_merchants(n=5),
        "monthly_totals": metrics.monthly_totals(),
        "fastest_growing_category": metrics.fastest_growing_category(),
        "top_expenses_week": metrics.latest_week_top_expenses(k=3),
    }

    # Create a better prompt for LLM
    prompt = f"""
    You are a personal finance assistant. 
    Use the following transaction summary (JSON) to answer the user’s question.

    Transaction Summary:
    {json.dumps(context, indent=2)}

    Question: {req.query}

    Answer clearly, using the numbers from the data only.
    """

    answer = ask_llm(prompt)
    return {"answer": answer, "context_used": context}
