import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Smart Drilling Dashboard", layout="wide")

st.title("⛏ Smart Drilling IoT Dashboard")
st.write("Real-time monitoring of drilling parameters with predictive alerts.")

# Empty dataframe
data = pd.DataFrame(columns=["Time", "Depth", "RPM", "Torque"])

# Placeholders
chart_col, alert_col = st.columns([3, 1])
line_placeholder = chart_col.empty()
metrics_placeholder = alert_col.empty()

depth = 0
high_torque_count = 0

# Simulate streaming
for t in range(1, 61):  # 60 readings
    depth += np.random.randint(1, 5)
    rpm = np.random.randint(800, 1200)
    torque = np.random.randint(50, 200)

    new_row = {"Time": t, "Depth": depth, "RPM": rpm, "Torque": torque}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    # Track high torque for predictive maintenance
    if torque > 150:
        high_torque_count += 1
    else:
        high_torque_count = 0

    # Update charts
    with line_placeholder.container():
        st.subheader("📊 Live Drilling Data")
        st.line_chart(data.set_index("Time")[["Depth", "RPM", "Torque"]])

    # Update metrics + alerts
    with metrics_placeholder.container():
        st.subheader("⚙ Current Status")
        st.metric("Depth (m)", depth)
        st.metric("RPM", rpm)
        st.metric("Torque (Nm)", torque)

        if torque > 150:
            st.error(f"⚠ High Torque Alert: {torque} Nm")
        if high_torque_count >= 3:
            st.warning("🔮 Predictive Alert: Possible Drill Failure Soon!")

    time.sleep(0.5)

# After simulation: Allow export
st.subheader("📂 Export Data")
csv = data.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "drilling_data.csv", "text/csv")