
import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# Config
st.set_page_config(page_title="JJ's Trading Dashboard v7", layout="wide")

# Title
st.title("📈 JJ's Live Trading Dashboard v7")

# Trading log file path (assumed to be local for now)
TRADING_LOG_FILE = "trading_log.txt"

def load_trading_log():
    try:
        df = pd.read_csv(TRADING_LOG_FILE, sep="|", header=None, engine="python")
        df.columns = ["Timestamp", "Details"]
        df["Timestamp"] = pd.to_datetime(df["Timestamp"].str.extract(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})")[0])
        return df
    except Exception as e:
        st.warning(f"Could not load trading log: {e}")
        return pd.DataFrame(columns=["Timestamp", "Details"])

def plot_profit_curve(df):
    if df.empty:
        st.info("No trades yet to plot.")
        return

    # Dummy profit calculation for now (can upgrade later)
    df["PnL"] = (df.index + 1) * 10  # Example growing P/L
    fig = px.line(df, x="Timestamp", y="PnL", title="Profit/Loss Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.header("💼 Account Overview")
    st.metric(label="Equity", value="$100,000")
    st.metric(label="Buying Power", value="$200,000")
    st.metric(label="Cash", value="$100,000")

with col2:
    st.header("📝 Recent Trades")
    df_log = load_trading_log()
    st.dataframe(df_log.tail(10))

st.divider()

st.header("📊 Profit/Loss Curve")
plot_profit_curve(df_log)

st.divider()

# Force Refresh Button
if st.button("🔄 Force Refresh"):
    st.experimental_rerun()

# Auto-refresh every 5 minutes (300 seconds)
st_autorefresh = st.empty()
st_autorefresh.markdown(f"⏳ Auto-refreshing every 5 minutes...")
time.sleep(300)
st.experimental_rerun()
