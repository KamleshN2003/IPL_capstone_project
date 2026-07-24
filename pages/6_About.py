import streamlit as st

st.set_page_config(
    page_title="About Project",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ About IPL 2022 Analytics Dashboard")

st.markdown("""
## 📌 Project Overview

This dashboard analyzes the IPL 2022 season using interactive visualizations
built with Python and Streamlit.

The objective is to help users explore:

- 🏏 Team Performance
- ⭐ Player Performance
- 🏟 Venue Statistics
- 📈 Match Insights
- 📊 Data Exploration

The dashboard is designed for learning Data Analytics and Data Visualization.
""")

st.divider()

st.subheader("🛠 Tech Stack")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
### Languages

- Python
- SQL
""")

    st.markdown("""
### Libraries

- Pandas
- Plotly
- Streamlit
""")

with col2:
    st.markdown("""
### Concepts

- Data Cleaning
- Exploratory Data Analysis
- Data Visualization
- Dashboard Development
""")

st.divider()

st.subheader("📂 Dataset")

st.write("""
Dataset contains IPL 2022 match information including:

- Match ID
- Date
- Venue
- Teams
- Toss Winner
- Match Winner
- Player of the Match
- Top Scorer
- Best Bowler
- Match Stage
""")

st.divider()

st.subheader("🎯 Project Features")

st.markdown("""
✅ Multi-page Dashboard

✅ Team Analysis

✅ Player Analysis

✅ Venue Analysis

✅ Interactive Charts

✅ Download Reports

✅ Business Insights
""")

st.divider()

st.subheader("👨‍💻 Developer")

st.success("""
Kamlesh Nayak

MCA Graduate

Python Developer

Data Analytics Enthusiast
""")