
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from health_engine import assess_health

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="ASTROVITAL",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #081426;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #10233d;
}

h1, h2, h3 {
    color: #70d6ff;
}

div.stButton > button {
    background-color: #087ea4;
    color: white;
    border-radius: 8px;
    height: 48px;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #0aa4ce;
    color: white;
}

[data-testid="stMetric"] {
    background-color: #142b46;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------

st.title("🚀 ASTROVITAL")

st.subheader(
    "Astronaut Health Intelligence & Early Warning System"
)

st.write(
    "🛰️ Smart Health Monitoring for Space Missions"
)

st.info(
    "DEMO MODE: This prototype uses manually entered health readings "
    "and simulated historical data. It does not use live wearable sensors."
)


# ---------------- SIDEBAR ----------------

st.sidebar.title("🛰️ Mission Control")

astronaut = st.sidebar.text_input(
    "Astronaut Name",
    "Demo Astronaut"
)

mission = st.sidebar.selectbox(
    "Select Mission",
    [
        "International Space Station",
        "Lunar Mission",
        "Mars Mission"
    ]
)

mission_day = st.sidebar.number_input(
    "Mission Day",
    min_value=1,
    max_value=1000,
    value=12
)

st.sidebar.markdown("---")

st.sidebar.write("**System:** ASTROVITAL")
st.sidebar.write("**Mode:** Research Prototype")
st.sidebar.write("**Status:** Demo Monitoring")


# ---------------- ASTRONAUT PROFILE ----------------

st.markdown("---")
st.header("👨‍🚀 Astronaut Profile")

p1, p2, p3 = st.columns(3)

with p1:
    st.metric("Astronaut", astronaut)

with p2:
    st.metric("Mission", mission)

with p3:
    st.metric("Mission Day", mission_day)


# ---------------- HEALTH INPUT ----------------

st.markdown("---")
st.header("📊 Astronaut Health Monitoring")

st.write("Enter the astronaut's sample health readings below.")

with st.form("health_form"):

    c1, c2, c3 = st.columns(3)

    with c1:
        heart_rate = st.number_input(
            "❤️ Heart Rate (BPM)",
            min_value=30,
            max_value=180,
            value=75
        )

    with c2:
        spo2 = st.number_input(
            "🫁 Oxygen Level (SpO₂ %)",
            min_value=70,
            max_value=100,
            value=98
        )

    with c3:
        temperature = st.number_input(
            "🌡️ Body Temperature (°C)",
            min_value=34.0,
            max_value=42.0,
            value=36.8,
            step=0.1
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        sleep = st.slider(
            "😴 Sleep Duration (hours)",
            0.0,
            12.0,
            7.0
        )

    with c5:
        stress = st.slider(
            "🧠 Stress Level",
            1,
            10,
            3
        )

    with c6:
        fatigue = st.slider(
            "⚡ Fatigue Level",
            1,
            10,
            3
        )

    analyse = st.form_submit_button(
        "🔍 ANALYSE ASTRONAUT HEALTH",
        use_container_width=True
    )


# ---------------- HEALTH ANALYSIS ----------------

if analyse:

    result = assess_health(
        heart_rate,
        spo2,
        temperature,
        sleep,
        stress,
        fatigue
    )

    risk = result["risk_level"]

    st.markdown("---")
    st.header("🧬 Health Analysis Results")

    if risk == "ATTENTION REQUIRED":
        st.error("⚠️ ATTENTION REQUIRED")

    elif risk == "MONITOR HEALTH":
        st.warning("🟡 MONITOR HEALTH")

    else:
        st.success("🟢 WITHIN DEMO RULES")

    # HEALTH SUMMARY

    st.subheader("Health Summary")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Heart Rate", f"{heart_rate} BPM")

    with m2:
        st.metric("Oxygen Level", f"{spo2}%")

    with m3:
        st.metric("Temperature", f"{temperature} °C")

    m4, m5, m6 = st.columns(3)

    with m4:
        st.metric("Sleep", f"{sleep} hours")

    with m5:
        st.metric("Stress", f"{stress}/10")

    with m6:
        st.metric("Fatigue", f"{fatigue}/10")

    # DETECTED INDICATORS

    st.markdown("---")
    st.subheader("⚠️ Detected Health Indicators")

    if result["issues"]:

        for issue in result["issues"]:
            st.warning("• " + issue)

    else:
        st.success(
            "No indicators were triggered by the demo rules."
        )

    # RECOMMENDATIONS

    st.markdown("---")
    st.subheader("💡 Recommendations")

    for recommendation in result["recommendations"]:
        st.write("• " + recommendation)

    st.caption(
        "These are illustrative prototype rules, not clinical "
        "or NASA operational thresholds."
    )

    # DOWNLOAD REPORT

    st.markdown("---")
    st.subheader("📥 Download Health Report")

    report = f"""
ASTROVITAL
ASTRONAUT HEALTH MONITORING REPORT

Date: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}

ASTRONAUT DETAILS
-------------------------
Astronaut: {astronaut}
Mission: {mission}
Mission Day: {mission_day}

HEALTH READINGS
-------------------------
Heart Rate: {heart_rate} BPM
Oxygen Level: {spo2}%
Body Temperature: {temperature} C
Sleep Duration: {sleep} hours
Stress Level: {stress}/10
Fatigue Level: {fatigue}/10

HEALTH ASSESSMENT
-------------------------
Risk Level: {risk}

DETECTED INDICATORS
-------------------------
{chr(10).join(result["issues"]) if result["issues"] else "No indicators triggered"}

RECOMMENDATIONS
-------------------------
{chr(10).join(result["recommendations"])}

DISCLAIMER
-------------------------
This report is generated by an educational prototype.
The readings and rules are not clinically validated.
This system is not a medical device and must not be
used for medical diagnosis or treatment.
"""

    st.download_button(
        label="📥 Download ASTROVITAL Report",
        data=report,
        file_name="ASTROVITAL_Health_Report.txt",
        mime="text/plain",
        use_container_width=True
    )


# ---------------- HEALTH TREND CHARTS ----------------

st.markdown("---")
st.header("📈 Mission Health Trends")

st.caption(
    "Illustrative simulated data only. These are not actual "
    "astronaut measurements."
)

dates = [
    (datetime.now() - timedelta(days=i)).strftime("%d %b")
    for i in range(6, -1, -1)
]

trend_data = pd.DataFrame({
    "Date": dates,
    "Heart Rate": [
        random.randint(65, 90) for _ in dates
    ],
    "Oxygen Level": [
        random.randint(95, 99) for _ in dates
    ],
    "Temperature": [
        round(random.uniform(36.4, 37.2), 1)
        for _ in dates
    ]
})

tab1, tab2, tab3 = st.tabs([
    "❤️ Heart Rate",
    "🫁 Oxygen Level",
    "🌡️ Temperature"
])

with tab1:
    st.line_chart(
        trend_data.set_index("Date")[["Heart Rate"]]
    )

with tab2:
    st.line_chart(
        trend_data.set_index("Date")[["Oxygen Level"]]
    )

with tab3:
    st.line_chart(
        trend_data.set_index("Date")[["Temperature"]]
    )


# ---------------- NASA RESEARCH INTEGRATION ----------------

st.markdown("---")

st.subheader("🛰️ NASA OSD-574 | Inspiration4 Microbiome Study")

st.info(
    "Research dataset: NASA OSD-574. "
    "This study examines skin microbiome data from four Inspiration4 crew members. "
    "It is not live astronaut vital-sign data."
)

st.markdown("### Dataset summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Crew members", "4")

with col2:
    st.metric("Metagenomic samples", "8")

with col3:
    st.metric("Sampling time points", "2")

st.markdown("### Sampling details")

st.write("""
- Pre-flight: L-44
- Post-flight: R+1
- Sample type: Deltoid skin microbiome
- Data type: Metagenomic sequencing
""")

st.markdown("### Reported research observation")

st.write("""
The uploaded research documentation reports an increase in the
mean human-read fraction from approximately 31% before flight
to 62% after flight.

These are reported research-document values, not results
independently calculated by this application.
""")

st.warning(
    "This dataset does not provide live heart rate, SpO₂ or "
    "body-temperature measurements. No clinical conclusion "
    "should be drawn from these microbiome observations."
)

st.markdown("### NASA research sources")

st.markdown("[NASA Open Science Data Repository](https://osdr.nasa.gov/)")

st.markdown("[NASA OSD-574 study](https://osdr.nasa.gov/bio/repo/data/studies/OSD-574)")

st.markdown("[NASA Human Research Program](https://www.nasa.gov/hrp/)")

st.write(
    "**Study title:** SpaceX Inspiration4 Deltoid Skin and Microbiome Data"
)

st.write("""
**Research details:**

- Mission: SpaceX Inspiration4
- Mission duration: 3 days
- Crew: Four private astronauts
- Research sample: Deltoid skin biopsies and skin swabs
- Pre-flight biopsy: L-44
- Post-flight biopsy: R+1
- Research methods: Spatial transcriptomics,
  metagenomics and metatranscriptomics
- Organisms: Human and microbiota
""")

st.info(
    "Research insight: OSD-574 studies skin-related biological "
    "and microbiome changes associated with spaceflight. "
    "It does not provide live heart rate or SpO₂ readings."
)

st.markdown(
    "[🔗 Open Official NASA OSD-574 Dataset]"
    "(https://osdr.nasa.gov/bio/repo/data/studies/OSD-574)"
)

st.markdown(
    "[🔗 NASA Open Science Data Repository]"
    "(https://osdr.nasa.gov/)"
)

st.markdown(
    "[🔗 NASA Human Research Program]"
    "(https://www.nasa.gov/hrp/)"
)


# ---------------- FOOTER ----------------

st.markdown("---")

st.caption(
    "ASTROVITAL | Student Space Research Prototype | 2026"
)

st.caption(
    "Educational demonstration only. Not a medical device. "
    "Not intended for medical diagnosis or treatment."
)
