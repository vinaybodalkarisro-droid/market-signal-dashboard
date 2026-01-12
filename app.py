import streamlit as st
from market_news_intel import build_market_table

st.set_page_config(page_title="Market Signal Dashboard", layout="wide")

# ---------------- THEME ----------------
st.markdown("""
<style>
.stApp { background-color: #0f172a; }
html, body, [class*="css"] { color: #e5e7eb !important; }

.card {
    background-color: #020617;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
    border-left: 5px solid #38bdf8;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
}

.bullish { color: #22c55e; font-weight: 700; }
.bearish { color: #ef4444; font-weight: 700; }
.neutral { color: #eab308; font-weight: 700; }

.date { color: #94a3b8; font-size: 12px; }

a { color: #38bdf8 !important; text-decoration: none; font-weight: 600; }
h1, h2, h3, h4 { color: #f8fafc !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.title("📊 Market News Signal Dashboard")
st.caption("Headline + Signal + Date | Gold • Silver • Crude Oil • Crypto • India")

# ---------------- SIDEBAR ----------------
market = st.sidebar.selectbox("Select Market", ["Metals", "Crypto", "India"])

asset_map = {
    "Metals": ["Gold", "Silver", "Crude Oil"],
    "Crypto": ["Crypto"],
    "India": ["India Markets"]
}

asset = st.sidebar.selectbox("Select Asset", asset_map[market])

direction_filter = st.sidebar.multiselect(
    "Signal Type",
    ["Bullish", "Bearish", "Neutral"],
    default=["Bullish", "Bearish"]
)

# ---------------- DATA ----------------
df = build_market_table(market, asset)

if not df.empty:
    df = df[df["Direction"].isin(direction_filter)]

# ---------------- DISPLAY ----------------
st.subheader(f"{asset} – Live Signals")

if df.empty:
    st.warning("No signals available.")
else:
    for _, row in df.iterrows():
        cls = "bullish" if row["Direction"] == "Bullish" else "bearish" if row["Direction"] == "Bearish" else "neutral"

        st.markdown(f"""
        <div class="card">
            <div class="date">{row['Date']}</div>
            <h4>{row['Title']}</h4>
            <div class="{cls}">{row['Direction']} Signal</div>
            🔗 <a href="{row['Link']}" target="_blank">Open News</a>
        </div>
        """, unsafe_allow_html=True)
