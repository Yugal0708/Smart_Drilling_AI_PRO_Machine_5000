import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Smart Drilling Dashboard", layout="wide")

st.title("⛏ Smart Drilling IoT Dashboard")
st.write("Real-time monitoring of drilling parameters with predictive alerts.")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = []
    st.session_state.depth = 0
    st.session_state.high_torque_count = 0

# Layout
chart_col, alert_col = st.columns([3, 1])

# Generate new data point
t = len(st.session_state.data) + 1

st.session_state.depth += np.random.randint(1, 5)
rpm = np.random.randint(800, 1200)
torque = np.random.randint(50, 200)

new_row = {
    "Time": t,
    "Depth": st.session_state.depth,
    "RPM": rpm,
    "Torque": torque
}

st.session_state.data.append(new_row)

# Convert to DataFrame
data = pd.DataFrame(st.session_state.data)


if torque > 150:
    st.session_state.high_torque_count += 1
else:
    st.session_state.high_torque_count = 0

#  Chart
with chart_col:
    st.subheader("📊 Live Drilling Data")
    st.line_chart(data.set_index("Time")[["Depth", "RPM", "Torque"]])

# ⚙ Metrics + Alerts
with alert_col:
    st.subheader("⚙ Current Status")
    st.metric("Depth (m)", st.session_state.depth)
    st.metric("RPM", rpm)
    st.metric("Torque (Nm)", torque)

    if torque > 150:
        st.error(f"⚠ High Torque Alert: {torque} Nm")

    if st.session_state.high_torque_count >= 3:
        st.warning("🔮 Predictive Alert: Possible Drill Failure Soon!")


time.sleep(0.5)
st.rerun()

# Export
st.subheader("📂 Export Data")
csv = data.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "drilling_data.csv", "text/csv")
