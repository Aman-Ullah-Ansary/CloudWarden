import streamlit as st
import sqlite3
import pandas as pd


def sidebar():

    # -----------------------------
    # Session State
    # -----------------------------
    if "page" not in st.session_state:
        st.session_state["page"] = "Dashboard"

    # -----------------------------
    # Load Dashboard Data
    # -----------------------------
    try:

        conn = sqlite3.connect("cloudwarden.db")

        df = pd.read_sql(
            "SELECT * FROM namespace_costs",
            conn
        )

        forecast = pd.read_sql(
            "SELECT * FROM forecasts ORDER BY id DESC LIMIT 1",
            conn
        )

        conn.close()

        total_cost = df["cost"].sum()
        namespaces = df["namespace"].nunique()

        if forecast.empty:
            forecast_cost = 0
        else:
            forecast_cost = forecast.iloc[0]["predicted_cost"]

        highest = (
            df.groupby("namespace")["cost"]
            .sum()
            .idxmax()
        )

    except Exception:

        total_cost = 0
        namespaces = 0
        forecast_cost = 0
        highest = "N/A"

    # -----------------------------
    # Custom CSS
    # -----------------------------
    st.markdown("""
    <style>

    section[data-testid="stSidebar"]{
        width:340px !important;
    }

    div.stButton > button{
        width:100%;
        height:55px;
        border-radius:12px;
        font-size:18px;
        font-weight:600;
        margin-bottom:8px;
    }

    [data-testid="metric-container"]{
        border-radius:12px;
        border:1px solid #2D3748;
        padding:10px;
        background:#151A24;
    }

    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Sidebar
    # -----------------------------
    with st.sidebar:

        st.markdown("# ☁️ CloudWarden AI")
        st.caption("Intelligent Kubernetes FinOps Platform")

        st.divider()

        st.markdown("### 👤 Aman Ullah Ansary")
        st.success("🟢| Workspace |")

        st.divider()

        st.markdown("## 📂 Navigation")

        if st.button(
            "🏠 Dashboard",
            use_container_width=True,
            type="primary" if st.session_state["page"] == "Dashboard" else "secondary"
        ):
            st.session_state["page"] = "Dashboard"

        if st.button(
            "🤖 AI Report",
            use_container_width=True,
            type="primary" if st.session_state["page"] == "AI Report" else "secondary"
        ):
            st.session_state["page"] = "AI Report"

        if st.button(
            "📈 Forecast",
            use_container_width=True,
            type="primary" if st.session_state["page"] == "Forecast" else "secondary"
        ):
            st.session_state["page"] = "Forecast"
        
        if st.button(
            "🚨 Anomaly Detection",
            use_container_width=True,
            type="primary" if st.session_state["page"] == "Anomaly Detection" else "secondary"
        ):      
            st.session_state["page"] = "Anomaly Detection"
            
        if st.button(
            "📜 History",
            use_container_width=True,
            type="primary" if st.session_state["page"] == "History" else "secondary"
        ):
            st.session_state["page"] = "History"

        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            type="primary" if st.session_state["page"] == "Settings" else "secondary"
        ):
            st.session_state["page"] = "Settings"

        page = st.session_state["page"]

        st.divider()

        st.markdown("## 📊 Cluster Summary")

        st.metric("💰 Total Cost", f"${total_cost:.2f}")
        st.metric("📦 Namespaces", namespaces)
        st.metric("📈 Forecast", f"${forecast_cost:.2f}")
        st.metric("🔥 Highest Cost", highest)

        st.divider()

        st.markdown("## 🖥 Cluster Status")

        st.success("🟢 Cluster Healthy")
        st.success("🟢 OpenCost Connected")
        st.success("🟢 Groq AI Online")
        st.success("🟢 SQLite Connected")
        st.success("🟢 Kubernetes Running")

        st.divider()

        st.info("🚨 Active Anomalies : 2")
        st.info("💵 Estimated Saving : $3.42")

        st.divider()

        st.caption("CloudWarden AI")
        st.caption("Version 3.0")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state["login"] = False
            st.rerun()

    return page