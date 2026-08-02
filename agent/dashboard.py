import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import sqlite3
import plotly.express as px

from ai_agent import AIAgent
from pdf_report import PDFReport
from sidebar import sidebar
from login import login

st.set_page_config(
    page_title="CloudWarden AI",
    page_icon="☁️",
    layout="wide"
)

# ==========================================================
# GLOBAL STYLING  (Fix 7: rounded cards, shadows, hover, fonts)
# ==========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---------- KPI / Metric Cards ---------- */
.cw-card {
    position: relative;
    background: linear-gradient(160deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 22px;
    margin-bottom: 10px;
    backdrop-filter: blur(6px);
    box-shadow: 0 4px 18px rgba(0,0,0,0.28);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    overflow: hidden;
}

.cw-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #2dd4bf);
    opacity: 0.9;
}

.cw-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 28px rgba(0,0,0,0.4);
    border-color: var(--accent, #2dd4bf);
}

.cw-card-icon {
    font-size: 22px;
    margin-bottom: 6px;
}

.cw-card-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.55);
    margin-bottom: 6px;
}

.cw-card-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 25px;
    font-weight: 700;
    color: #f8fafc;
    line-height: 1.15;
}

.cw-card-delta {
    margin-top: 8px;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--accent, #2dd4bf);
}

/* ---------- Buttons ---------- */
div.stButton > button, div.stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.12);
    font-weight: 600;
    transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
}

div.stButton > button:hover, div.stDownloadButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.35);
    border-color: #2dd4bf;
    color: #2dd4bf;
}

/* ---------- Headers / dividers ---------- */
h1, h2, h3 {
    font-weight: 800 !important;
    letter-spacing: -0.01em;
}

hr {
    border-color: rgba(255,255,255,0.08) !important;
}
</style>
""", unsafe_allow_html=True)


def metric_card(icon, label, value, delta=None, accent="#2dd4bf"):
    """Styled KPI card used in place of st.metric (Fix 3 / Fix 6)."""
    delta_html = f'<div class="cw-card-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="cw-card" style="--accent:{accent}">
            <div class="cw-card-icon">{icon}</div>
            <div class="cw-card-label">{label}</div>
            <div class="cw-card-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True
    )


st_autorefresh(
    interval=30000,
    key="refresh"
)

# ----------------------------
# Session State
# ----------------------------

if "login" not in st.session_state:
    st.session_state["login"] = False

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "ai_answer" not in st.session_state:
    st.session_state["ai_answer"] = ""

if not st.session_state["login"]:
    login()
    st.stop()

page = sidebar()

# Fix 1: Dashboard "Quick Action" buttons can jump to another page
if "quick_action_page" in st.session_state:
    page = st.session_state.pop("quick_action_page")

conn = sqlite3.connect("cloudwarden.db")

df = pd.read_sql(
    "SELECT * FROM namespace_costs",
    conn
)

forecast = pd.read_sql(
    "SELECT * FROM forecasts ORDER BY id DESC LIMIT 1",
    conn
)

total_cost = df["cost"].sum()
total_namespaces = df["namespace"].nunique()

forecast_cost = 0
if not forecast.empty:
    forecast_cost = forecast.iloc[0]["predicted_cost"]

summary = (
    df.groupby("namespace")["cost"]
      .sum()
      .reset_index()
)

# ==========================================================
# DASHBOARD
# ==========================================================

if page == "Dashboard":

    highest_namespace = summary.sort_values("cost", ascending=False).iloc[0]
    anomaly_count = len(df[df["cost"] > df["cost"].mean() * 1.5])

    # ------------------------------------------------------
    # Welcome Banner
    # ------------------------------------------------------

    st.markdown("## ☁️ CloudWarden-AI Dashboard")
    st.markdown("#### Welcome back, Aman 👋")
    st.caption("Monitor • Predict • Optimize Kubernetes Cloud Costs")

    st.success("🟢 Kubernetes Cluster Healthy   |   OpenCost Connected   |   Groq AI Online")

    st.divider()

    # ------------------------------------------------------
    # KPI Cards (Fix 3: styled cards instead of st.metric)
    # ------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("💰", "Total Cost", f"${total_cost:.2f}", accent="#2dd4bf")

    with c2:
        metric_card("📦", "Namespaces", f"{total_namespaces}", accent="#8b5cf6")

    with c3:
        metric_card("📈", "Forecast", f"${forecast_cost:.2f}", accent="#f59e0b")

    with c4:
        anomaly_accent = "#22c55e" if anomaly_count == 0 else "#f43f5e"
        metric_card("🚨", "Anomalies", f"{anomaly_count}", accent=anomaly_accent)

    st.divider()

    # ------------------------------------------------------
    # Charts
    # ------------------------------------------------------

    left, right = st.columns(2)

    with left:
        st.subheader("📊 Namespace Cost")
        st.bar_chart(summary.set_index("namespace"))

    with right:
        st.subheader("🥧 Cost Distribution")
        fig_pie = px.pie(
            summary,
            values="cost",
            names="namespace",
            hole=0.55,
            template="plotly_dark"
        )
        fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_pie, width="stretch")

    st.divider()

    st.subheader("📈 Cost Trend")

    trend = (
        df.groupby("created_at")["cost"]
          .sum()
          .reset_index()
    )

    trend["created_at"] = pd.to_datetime(trend["created_at"])
    trend = trend.sort_values("created_at")

    # Fix 2: Plotly line chart instead of st.line_chart
    fig_trend = px.line(
        trend,
        x="created_at",
        y="cost",
        markers=True,
        template="plotly_dark"
    )
    fig_trend.update_traces(line_color="#2dd4bf", line_width=3)
    fig_trend.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_trend, width="stretch")

    st.divider()

    # ------------------------------------------------------
    # Bottom Cards
    # ------------------------------------------------------

    b1, b2 = st.columns(2)

    with b1:
        st.subheader("🔥 Highest Cost Namespace")
        st.info(
            f"### {highest_namespace['namespace']}\n"
            f"Current Cost\n\n"
            f"**${highest_namespace['cost']:.2f}**"
        )

    with b2:
        st.subheader("🤖 AI Quick Insight")
        percent = (highest_namespace["cost"] / total_cost) * 100 if total_cost else 0
        st.success(
            f"**{highest_namespace['namespace']}** accounts for **{percent:.1f}%** "
            f"of total cluster cost.\n\nPotential optimization opportunity detected."
        )

    st.divider()

    # ------------------------------------------------------
    # Quick Actions (Fix 1: now actually wired up)
    # ------------------------------------------------------

    st.subheader("⚡ Quick Actions")

    q1, q2, q3 = st.columns(3)

    with q1:
        if st.button("📄 Generate AI Report", use_container_width=True):
            st.session_state["quick_action_page"] = "AI Report"
            st.rerun()

    with q2:
        if st.button("🤖 Open AI Assistant", use_container_width=True):
            st.session_state["quick_action_page"] = "AI Report"
            st.rerun()

    with q3:
        export_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export CSV",
            export_csv,
            file_name="cluster_cost.csv",
            mime="text/csv",
            use_container_width=True
        )

# ==========================================================
# AI REPORT
# ==========================================================

elif page == "AI Report":

    st.title("🤖 CloudWarden AI Copilot")
    st.caption("Ask questions about your Kubernetes cluster, cloud costs, AWS, DevOps and FinOps.")

    report = "\n".join(
        [f"{row.namespace}: ${row.cost:.5f}" for row in summary.itertuples()]
    )

    ai = AIAgent()

    left, right = st.columns([1, 2])

    # ------------------------------------------------------
    # LEFT PANEL
    # ------------------------------------------------------

    with left:

        st.subheader("📄 AI Executive Summary")

        if st.button("⚡ Generate Executive Report", use_container_width=True):

            with st.spinner("Generating report..."):
                response = ai.analyze(report)

            st.session_state["ai_answer"] = response

            pdf = PDFReport()
            filename = pdf.generate(response)

            with open(filename, "rb") as file:
                st.download_button(
                    "📄 Download PDF",
                    file,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )

        st.divider()

        # Fix 4: renamed section + explicit Question / Answer labels
        st.subheader("💬 Conversation History")

        history = list(reversed(st.session_state["chat_history"]))

        if len(history) == 0:
            st.info("No conversations yet.")
        else:
            for chat in history[:5]:
                with st.expander(f"👤 {chat['question']}"):
                    st.markdown(f"**🤖 Answer**\n\n{chat['answer']}")

        if len(history) > 5:
            with st.expander("📂 Show All Chats"):
                search = st.text_input("Search Chat", key="chat_search")
                for chat in history:
                    if (
                        search == ""
                        or search.lower() in chat["question"].lower()
                        or search.lower() in chat["answer"].lower()
                    ):
                        st.markdown(f"### 👤 {chat['question']}")
                        st.markdown(f"🤖 {chat['answer']}")
                        st.divider()

        if st.button("🗑 Clear Chat History", use_container_width=True):
            st.session_state["chat_history"] = []
            st.session_state["ai_answer"] = ""
            st.rerun()

    # ------------------------------------------------------
    # RIGHT PANEL
    # ------------------------------------------------------

    with right:

        st.subheader("💬 CloudWarden AI Assistant")

        question = st.text_input(
            "Ask your question",
            placeholder="Example: Which namespace is increasing cloud cost?"
        )

        if st.button("🚀 Ask CloudWarden AI", use_container_width=True):

            if question.strip() == "":
                st.warning("Please enter a question.")
            else:
                with st.spinner("CloudWarden AI is thinking..."):
                    answer = ai.chat(question, report)

                st.session_state["ai_answer"] = answer
                st.session_state["chat_history"].append(
                    {"question": question, "answer": answer}
                )
                st.rerun()

        st.divider()

        if st.session_state["ai_answer"] != "":
            st.markdown("### 🤖 AI Response")
            with st.container():
                st.markdown(st.session_state["ai_answer"])
        else:
            st.info("Start a conversation with CloudWarden AI.")

# ==========================================================
# ANOMALY DETECTION
# ==========================================================

elif page == "Anomaly Detection":

    st.title("🚨 CloudWarden Anomaly Detection Center")
    st.caption("Real-time AI powered Kubernetes cost anomaly monitoring.")

    st.divider()

    avg_cost = df["cost"].mean()
    threshold = avg_cost * 1.50
    anomalies = df[df["cost"] > threshold]
    anomaly_count = len(anomalies)
    estimated_saving = anomalies["cost"].sum() * 0.30

    # Fix 5: 3-tier health status driven by the share of cost that's anomalous
    anomaly_cost_share = (anomalies["cost"].sum() / total_cost) if total_cost else 0

    if anomaly_count == 0:
        cluster_health = "🟢 Healthy"
        health_accent = "#22c55e"
    elif anomaly_cost_share < 0.15:
        cluster_health = "🟡 Warning"
        health_accent = "#f59e0b"
    else:
        cluster_health = "🔴 Critical"
        health_accent = "#f43f5e"

    # ------------------------------------------------------
    # KPI Cards
    # ------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("🚨", "Active Alerts", f"{anomaly_count}", accent="#f43f5e")

    with c2:
        metric_card("💵", "Estimated Saving", f"${estimated_saving:.2f}", accent="#2dd4bf")

    with c3:
        metric_card("📦", "Total Namespaces", f"{total_namespaces}", accent="#8b5cf6")

    with c4:
        metric_card("🩺", "Cluster Health", cluster_health, accent=health_accent)

    st.divider()

    # ------------------------------------------------------
    # Status Banner
    # ------------------------------------------------------

    if anomaly_count == 0:
        st.success("✅ No anomalies detected. Everything looks healthy.")
    elif cluster_health == "🟡 Warning":
        st.warning(f"🟡 {anomaly_count} cost anomalies detected. Monitor closely.")
    else:
        st.error(f"🔴 {anomaly_count} cost anomalies detected. Immediate action recommended.")

    # ------------------------------------------------------
    # Cost Distribution
    # ------------------------------------------------------

    left, right = st.columns(2)

    with left:
        st.subheader("📊 Anomaly Cost")
        if anomaly_count == 0:
            st.info("No anomaly chart available.")
        else:
            st.bar_chart(anomalies.set_index("namespace")["cost"])

    with right:
        st.subheader("🥧 Cost Distribution")
        fig_pie2 = px.pie(
            summary,
            values="cost",
            names="namespace",
            hole=0.55,
            template="plotly_dark"
        )
        fig_pie2.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_pie2, width="stretch")

    st.divider()

    # ------------------------------------------------------
    # Table
    # ------------------------------------------------------

    st.subheader("📋 Detected Namespaces")

    if anomaly_count == 0:
        st.info("No anomaly data.")
    else:
        st.dataframe(anomalies, width="stretch")

    st.divider()

    # ------------------------------------------------------
    # AI Root Cause
    # ------------------------------------------------------

    st.subheader("🤖 AI Root Cause Analysis")

    if anomaly_count == 0:
        st.success("No AI analysis required.")
    else:
        report = "\n".join(
            [f"{row.namespace}: ${row.cost:.5f}" for row in anomalies.itertuples()]
        )

        ai = AIAgent()

        with st.spinner("CloudWarden AI is analyzing anomalies..."):
            analysis = ai.analyze(report)

        st.markdown(analysis)

    st.divider()

    # ------------------------------------------------------
    # Recommendations
    # ------------------------------------------------------

    st.subheader("🎯 Optimization Recommendations")

    if anomaly_count == 0:
        st.success("No optimization required.")
    else:
        st.info(
            "• Scale idle workloads\n"
            "• Reduce unused resources\n"
            "• Optimize requests & limits\n"
            "• Remove orphan PVCs\n"
            "• Enable Cluster Autoscaler\n"
            "• Schedule workloads efficiently\n"
            "• Monitor namespace growth\n"
            "• Review OpenCost allocation"
        )

    st.divider()

    # ------------------------------------------------------
    # Export
    # ------------------------------------------------------

    anomaly_csv = anomalies.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Export Anomaly Report",
        anomaly_csv,
        file_name="cloudwarden_anomalies.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==========================================================
# FORECAST
# ==========================================================

elif page == "Forecast":

    st.header("📈 Cost Forecast")

    metric_card("📈", "Predicted Next Cost", f"${forecast_cost:.2f}", accent="#f59e0b")

    st.info("Forecast generated using Linear Regression.")

    st.subheader("Forecast History")

    st.dataframe(
        forecast.sort_values("id", ascending=False),
        width="stretch"
    )

# ==========================================================
# HISTORY
# ==========================================================

elif page == "History":

    st.header("📜 Namespace Cost History")

    search = st.text_input("🔍 Search Namespace")

    history = df.copy()

    if search:
        history = history[
            history["namespace"].str.contains(search, case=False)
        ]

    st.dataframe(
        history.sort_values("id", ascending=False),
        width="stretch"
    )

    csv = history.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV",
        csv,
        file_name="namespace_history.csv",
        mime="text/csv"
    )

# ==========================================================
# SETTINGS
# ==========================================================

elif page == "Settings":

    st.header("⚙ Settings")

    st.success("CloudWarden AI is running successfully.")

    st.divider()

    # Fix 6: settings as a metric-card grid instead of plain st.write lines
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        metric_card("🏷️", "Version", "3.0", accent="#2dd4bf")

    with s2:
        metric_card("🤖", "AI Model", "Groq Llama-3.3-70B", accent="#8b5cf6")

    with s3:
        metric_card("🗄️", "Database", "SQLite", accent="#f59e0b")

    with s4:
        metric_card("🖥️", "Dashboard", "Streamlit", accent="#2dd4bf")

    s5, s6, s7, s8 = st.columns(4)

    with s5:
        metric_card("💸", "Cost Engine", "OpenCost", accent="#f43f5e")

    with s6:
        metric_card("📊", "Forecast Engine", "Scikit-learn", accent="#8b5cf6")

    with s7:
        metric_card("🔄", "Refresh Interval", "30 Seconds", accent="#f59e0b")

    with s8:
        metric_card("💾", "Chat History", "Session Memory", accent="#2dd4bf")

    st.divider()

    st.success("🟢 Groq AI Status : Online")

    st.divider()

    if st.button("🚪 Logout"):
        st.session_state["login"] = False
        st.rerun()

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "© 2026 CloudWarden AI | Intelligent Kubernetes FinOps Platform"
)

conn.close()