# 💰 Finance Chatbot

An AI-powered personal finance assistant that helps users analyze their spending, visualize financial trends, and interact with a chatbot for personalized finance insights. The project features a FastAPI backend for data processing and a Streamlit frontend for interactive visualization and chat.

---

## Features

- **Upload Transactions:** Securely upload CSV or Excel files of your financial transactions.
- **Spending Insights:** Visualize spending by category, monthly summaries, top merchants, weekly trends, and daily expenses.
- **AI Chatbot:** Ask finance-related questions and receive intelligent, context-aware answers.
- **Modern UI:** Clean, responsive dashboard built with Streamlit and Plotly.

---

## Project Structure

```
finance-chatbot/
│
├── app/                      # FastAPI backend
│   ├── __init__.py
│   ├── main.py               # FastAPI app entrypoint
│   ├── models/
│   │   └── schemas.py        # Pydantic models for data validation
│   ├── routers/              # API endpoints
│   │   ├── __init__.py
│   │   ├── chatbot.py        # /chatbot endpoint
│   │   ├── summary.py        # /summary endpoints
│   │   └── upload.py         # /upload endpoint
│   └── services/             # Business logic & utilities
│       ├── __init__.py
│       ├── .env              # Environment variables (API keys, etc.)
│       ├── data_store.py     # Data storage and retrieval
│       ├── llm.py            # Large Language Model (LLM) integration
│       └── metrics.py        # Financial metrics calculations
│
├── frontend/
│   └── user_interface.py     # Streamlit dashboard UI
│
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/finance-chatbot.git
cd finance-chatbot
```

### 2. Install Dependencies

It’s recommended to use a virtual environment:

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
pip install streamlit plotly  # For frontend
```

### 3. Configure Environment

- Edit `app/services/.env` to add any required API keys or environment variables.

### 4. Run the Backend (FastAPI)

```sh
uvicorn app.main:app --reload
```

- The API will be available at `http://127.0.0.1:8000`

### 5. Run the Frontend (Streamlit)

```sh
cd frontend
streamlit run user_interface.py
```

- The dashboard will open in your browser.

---

## API Endpoints

- **POST `/upload`**: Upload transaction files (CSV/XLSX).
- **GET `/summary/by-category`**: Get spending by category.
- **GET `/summary/monthly-totals`**: Get monthly expense totals.
- **GET `/summary/top-merchants?n=5`**: Get top merchants by spending.
- **GET `/summary/top-expenses-week?k=3`**: Get top weekly expenses.
- **GET `/summary/daily-totals`**: Get daily expense totals.
- **POST `/chatbot`**: Ask finance-related questions.

---

## File Descriptions

- `app/main.py`: FastAPI application setup and router inclusion.
- `app/routers/upload.py`: Handles file uploads.
- `app/routers/summary.py`: Provides summary statistics.
- `app/routers/chatbot.py`: Handles chatbot queries.
- `app/services/data_store.py`: Data storage and retrieval logic.
- `app/services/llm.py`: Integrates with LLM for chatbot responses.
- `app/services/metrics.py`: Computes financial metrics.
- `frontend/user_interface.py`: Streamlit UI for user interaction.

---

## Customization

- **LLM Integration:** Update `app/services/llm.py` and `.env` for your preferred LLM provider .
- **Data Storage:** By default, data is likely stored in-memory or in files. For production, integrate with a database in `app/services/data_store.py`.

---

## Screenshots

> Add screenshots of the dashboard and chatbot here.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)

-
