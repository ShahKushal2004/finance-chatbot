from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from app.services.data_store import save_transactions  # type: ignore
from app.models.schemas import UploadResponse

router = APIRouter()

@router.post("/", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = file.filename.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        elif filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file.file)
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

        rows = save_transactions(df)
        return UploadResponse(message="File uploaded successfully", rows=rows)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
