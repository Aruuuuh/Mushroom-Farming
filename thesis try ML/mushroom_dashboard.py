import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load and prepare dataset
df = pd.read_csv("pinning_fruiting_stage_dataset_realistic.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])

# App title
st.title("🍄 Mushroom Fruiting Housing - Dashboard")

# Page navigation
page = st.radio("Navigate", ["Environmental Sensors", "Harvest Prediction"], horizontal=True)

# Move downsample interval dropdown to page (not sidebar, not centered)
st.markdown("### Settings")
downsample_mapping = {
    '5 Minutes': '5T',
    '15 Minutes': '15T',
    '30 Minutes': '30T',
    '1 Hour': '1H'
}
selected_label = st.selectbox("Downsample Interval", list(downsample_mapping.keys()), index=2)
downsample_rate = downsample_mapping[selected_label]

# Downsample the data
df_downsampled = df.set_index('timestamp').resample(downsample_rate).mean().reset_index()

# Environmental Sensors Page
if page == "Environmental Sensors":
    st.subheader("Environmental Sensor Readings")

    fig1, ax1 = plt.subplots()
    sns.lineplot(data=df_downsampled, x='timestamp', y='temperature', ax=ax1)
    ax1.set_title("Temperature (°C)")
    ax1.set_ylabel("°C")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    sns.lineplot(data=df_downsampled, x='timestamp', y='humidity', ax=ax2)
    ax2.set_title("Humidity (%)")
    ax2.set_ylabel("%")
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots()
    sns.lineplot(data=df_downsampled, x='timestamp', y='co2', ax=ax3)
    ax3.set_title("CO₂ Concentration (ppm)")
    ax3.set_ylabel("ppm")
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots()
    sns.lineplot(data=df_downsampled, x='timestamp', y='light', ax=ax4)
    ax4.set_title("Light Intensity (Lux)")
    ax4.set_ylabel("Lux")
    st.pyplot(fig4)

# Harvest Prediction Page
elif page == "Harvest Prediction":
    st.subheader("Harvest Prediction")

    fig5, ax5 = plt.subplots()
    sns.lineplot(data=df_downsampled, x='timestamp', y='ready_to_harvest', ax=ax5)
    ax5.set_title("Predicted Readiness (0 = No, 1 = Yes)")
    ax5.set_ylim(-0.1, 1.1)
    ax5.set_ylabel("Ready to Harvest")
    st.pyplot(fig5)

# Footer
st.markdown("---")
st.markdown("📈 Data source: `pinning_fruiting_stage_dataset_realistic.csv`")
