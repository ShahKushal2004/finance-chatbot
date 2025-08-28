import streamlit as st
import plotly.express as px
import requests
import pandas as pd

BASE_URL = "http://127.0.0.1:8000"


# Streamlit page config
st.set_page_config(
    page_title="💰 Finance Assistant",
    page_icon="💵",
    layout="wide"
)

# Inject custom CSS for medium fonts & spacing
# Inject custom CSS for medium fonts, spacing & background
st.markdown(
    """
    <style>
    /* Background Gradient */
    .stApp {
        background: linear-gradient(to bottom right, #74ebd5, #ACB6E5);
    }

    /* Headings */
    h1, h2, h3 {
        font-size: 26px !important;
        color: #1f2937; /* dark gray */
        font-weight: 600;
    }

    /* Body text */
    p, span, div {
        font-size: 18px !important;
    }

    /* Success / Error messages */
    .stSuccess, .stError, .stWarning {
        font-size: 18px !important;
    }

    /* Chart containers */
    .stPlotlyChart {
        border-radius: 12px;
        padding: 10px;
        background: #f9fafb;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)




st.markdown("<h1 style='text-align: center;'>💰 AI-Powered Personal Finance Chatbot</h1>", unsafe_allow_html=True)

# =====================
# Upload Transactions
# =====================
# Upload Section Header with styling
st.markdown(
    "<h2 style='color:black; font-size:28px; font-weight:bold;'>📂 Upload Transactions</h2>", 
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your transactions (.csv / .xlsx)", 
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            uploaded_file.type
        )
    }
    response = requests.post(f"{BASE_URL}/upload", files=files)

    if response.status_code == 200:
        st.markdown(
            "<p style='color:green; font-size:18px; font-weight:bold;'>✅ Transactions uploaded successfully!</p>", 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<p style='color:red; font-size:18px; font-weight:bold;'>❌ Upload failed: {response.json().get('detail', response.text)}</p>", 
            unsafe_allow_html=True
        )


# =====================
# Spending Insights
# =====================


# Category Spending

# Category Spending
st.markdown("<h2 style='color:black; font-size:28px; font-weight:bold;'>📊 Spending Insights</h2>", unsafe_allow_html=True)

# Category Spending
res_cat = requests.get(f"{BASE_URL}/summary/by-category")
if res_cat.status_code == 200:
    data = res_cat.json()  # backend gives dict
    df_cat = pd.DataFrame(list(data.items()), columns=["Category", "Amount"])

    if not df_cat.empty:
        fig = px.pie(
            df_cat,
            names="Category",
            values="Amount",
            title="Spending by Category",
            hole=0.4
        )
        fig.update_traces(
            textinfo="percent+label",
            textfont=dict(size=18, color="black", family="Arial Black"),
            marker=dict(line=dict(color="black", width=2)),
            hovertemplate="<b>%{label}</b><br>💰 <b>Amount:</b> %{value}<br>📊 <b>Share:</b> %{percent}<extra></extra>"
        )
        fig.update_layout(
            title_font_size=28,
            legend=dict(
                title="Categories",
                font=dict(size=18, color="black", family="Arial Black")
            ),
            hoverlabel=dict(        # 🔹 control hover style
                font_size=16,
                font_family="Arial Black",
                font_color="black",
                bgcolor="white",    # white background
                bordercolor="black" # black border
            ),
            margin=dict(t=50, l=50, r=50, b=50)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No category data available.")
else:
    st.error("Failed to fetch category spending.")



# Monthly Totals
# Monthly Totals
st.markdown("<h2 style='color:black; font-size:28px; font-weight:bold;'>💰 Monthly Expense Summary</h2>", unsafe_allow_html=True)

res_month = requests.get(f"{BASE_URL}/summary/monthly-totals")
if res_month.status_code == 200:
    data = res_month.json()

    # If API response is dict, convert it properly
    if isinstance(data, dict):
        df_month = pd.DataFrame(list(data.items()), columns=["Month", "Total"])
    else:
        df_month = pd.DataFrame(data)

    if not df_month.empty:
        latest_month = df_month.iloc[-1]  # get the most recent month
        month_name = latest_month["Month"]
        total = latest_month["Total"]

        st.success(f"📢 Hey! Your total expense in **{month_name}** is **${total:,.2f}** 💸")
    else:
        st.warning("No monthly totals available.")
else:
    st.error("Failed to fetch monthly totals.")


# =====================
# Top Merchants
# =====================
st.markdown("<h2 style='color:black; font-size:28px; font-weight:bold;'>🏪 Top Merchants</h2>", unsafe_allow_html=True)
res_merch = requests.get(f"{BASE_URL}/summary/top-merchants?n=5")
if res_merch.status_code == 200:
    data = res_merch.json()

    # If response is dict → convert to DataFrame
    if isinstance(data, dict):
        df_merch = pd.DataFrame(list(data.items()), columns=["Merchant", "Amount"])
    else:  # assume list of dicts
        df_merch = pd.DataFrame(data)

    if not df_merch.empty:
        fig3 = px.bar(
            df_merch,
            x="Merchant" if "Merchant" in df_merch.columns else "merchant",
            y="Amount" if "Amount" in df_merch.columns else "amount",
            title="Top 5 Merchants",
            text_auto=True
        )

        # Modern styling
        fig3.update_traces(
            marker=dict(color="#10b981"),  # teal/green bars
            hovertemplate="<b>Merchant:</b> %{x}<br><b>Amount:</b> %{y}<extra></extra>"
        )

        fig3.update_layout(
            template="plotly_white",
            title_font=dict(size=24, color="#111"),
            font=dict(size=16),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(
                title="Merchant",
                title_font=dict(size=18, color="black", family="Arial Black"),
                tickfont=dict(size=14, color="black", family="Arial Black")
            ),
            yaxis=dict(
                title="Amount",
                title_font=dict(size=18, color="black", family="Arial Black"),
                tickfont=dict(size=14, color="black", family="Arial Black")
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial Black",
                font_color="black"
            )
        )

        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No merchant data available.")
else:
    st.error("Failed to fetch top merchants.")




# =====================
# Weekly Spending
# =====================
st.markdown("<h2 style='color:black; font-size:28px; font-weight:bold;'>📅 Weekly Spending Trends</h2>", unsafe_allow_html=True)

res_week = requests.get(f"{BASE_URL}/summary/top-expenses-week?k=3")
if res_week.status_code == 200:
    data = res_week.json()

    # Handle dict → convert into DataFrame
    if isinstance(data, dict):
        df_week = pd.DataFrame(list(data.items()), columns=["Week", "Amount"])
    else:  # assume list of dicts
        df_week = pd.DataFrame(data)

    if not df_week.empty:
        fig4 = px.bar(
            df_week,
            x="Week" if "Week" in df_week.columns else "week",
            y="Amount" if "Amount" in df_week.columns else "amount",
            title="Top Weekly Expenses",
            text_auto=True
        )

        # Update layout similar to line chart
        fig4.update_traces(
            marker=dict(color="#2563eb"),  # nice blue bars
            hovertemplate="<b>Week:</b> %{x}<br><b>Amount:</b> %{y}<extra></extra>"
        )

        fig4.update_layout(
            template="plotly_white",
            title_font=dict(size=24, color="#111"),
            font=dict(size=16),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(
                title="Type of Expense",
                title_font=dict(size=18, color="black", family="Arial Black"),
                tickfont=dict(size=14, color="black", family="Arial Black")
            ),
            yaxis=dict(
                title="Amount",
                title_font=dict(size=18, color="black", family="Arial Black"),
                tickfont=dict(size=14, color="black", family="Arial Black")
            ),
            hoverlabel=dict(
                bgcolor="white",
                font_size=14,
                font_family="Arial Black",
                font_color="black"
            )
        )

        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("No weekly expense data available.")
else:
    st.error("Failed to fetch weekly expenses.")



# =====================
# Daily Expenses
# =====================
st.markdown("<h2 style='color:black; font-size:28px; font-weight:bold;'>📈 Daily Expenses Trend</h2>", unsafe_allow_html=True)
res_daily = requests.get(f"{BASE_URL}/summary/daily-totals")
if res_daily.status_code == 200:
    df_daily = pd.DataFrame(res_daily.json())
    if not df_daily.empty:
        fig5 = px.line(df_daily, x="date", y="amount", title="Daily Expenses Trend", markers=True)

        # Customize line + markers
        fig5.update_traces(
            line=dict(width=3, color="#2563eb"),
            marker=dict(size=8, color="#ef4444"),
            hovertemplate="<b>Date:</b> %{x}<br><b>Amount:</b> %{y}<extra></extra>"
        )

        # Update layout for bold axis labels + hover label
        fig5.update_layout(
            template="plotly_white",
            title_font=dict(size=24, color="#111"),
            font=dict(size=16),
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(
                title="Date",
                title_font=dict(size=18, color="black", family="Arial Black"),
                tickfont=dict(size=14, color="black", family="Arial Black")
            ),
            yaxis=dict(
                title="Amount",
                title_font=dict(size=18, color="black", family="Arial Black"),
                tickfont=dict(size=14, color="black", family="Arial Black")
            ),
            hoverlabel=dict(
                bgcolor="white",      # White background
                font_size=14,         # Medium font
                font_family="Arial Black",
                font_color="black"    # Black bold text
            )
        )

        st.plotly_chart(fig5, use_container_width=True)


# =====================
# Chatbot
# =====================
st.markdown("<h2 style='color:black; font-size:28px; font-weight:bold;'>🤖 Ask your Finance Chatbot</h2>", unsafe_allow_html=True)

# Bigger input box
# Custom CSS for Ask button
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #ff4d4d;   /* 🔴 Red background */
        color: white;                /* White text */
        font-size: 18px;             /* Bigger text */
        font-weight: bold;           /* Bold */
        border-radius: 10px;         /* Rounded corners */
        height: 50px;
        width: 100%;
        border: 2px solid black;     /* Black border */
    }
    div.stButton > button:first-child:hover {
        background-color: #cc0000;   /* Darker red on hover */
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input box
user_input = st.text_area(
    "💬 Type your question here...",
    height=100,
    placeholder="e.g. What is my biggest expense this month?"
)

# Styled Ask button
if st.button("Ask"):
    if user_input.strip():
        response = requests.post(f"{BASE_URL}/chatbot", json={"query": user_input})
        if response.status_code == 200:
            answer = response.json().get("answer")

            # Styled response box
            st.markdown(
                f"""
                <div style="
                    padding: 15px;
                    border-radius: 10px;
                    background-color: #e6ffe6;
                    border: 2px solid #33cc33;
                    font-size: 18px;
                    font-weight: bold;
                    color: black;
                    margin-top: 10px;">
                    🤖 Answer: {answer}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("❌ Failed to fetch chatbot response.")


