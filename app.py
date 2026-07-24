"""
IPL Analytics Pro - Starter Home Page
Replace/add pages as needed.
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="IPL Analytics Pro",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CSS ----------
css_path = "assets/style.css"
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("IPL.csv")

df = load_data()

# ---------- SIDEBAR ----------
logo = "assets/logo.png"
if os.path.exists(logo):
    st.sidebar.image(logo, width=170)

st.sidebar.title("🏏 IPL Analytics Pro")

teams = sorted(pd.unique(pd.concat([df["team1"], df["team2"]])))

selected = st.sidebar.selectbox(
    "Select Team",
    ["All Teams"] + list(teams)
)

if selected != "All Teams":
    data = df[(df.team1 == selected) | (df.team2 == selected)]
else:
    data = df.copy()

# ---------- HERO ----------
st.markdown("""
<div style="
background:linear-gradient(135deg,#1E3A8A,#2563EB,#F59E0B);
padding:35px;
border-radius:20px;
text-align:center;
margin-bottom:25px;">
<h1 style="color:white;">🏏 IPL Analytics Pro</h1>
<p style="color:white;font-size:18px;">
Interactive Cricket Analytics Dashboard
</p>
</div>
""", unsafe_allow_html=True)

# ---------- KPI ----------
c1,c2,c3,c4 = st.columns(4)

c1.metric("Matches", len(data))
c2.metric("Teams", len(pd.unique(pd.concat([data.team1,data.team2]))))
c3.metric("Highest Score", int(data.first_ings_score.max()))
c4.metric("Average Score", round(data.first_ings_score.mean(),1))

st.divider()

# ---------- TEAM WINS ----------
wins = data.match_winner.value_counts().reset_index()
wins.columns=["Team","Wins"]

fig = px.bar(
    wins,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Matches Won by Team"
)
fig.update_layout(template="plotly_white")
st.plotly_chart(fig,use_container_width=True)

col1,col2=st.columns(2)

with col1:
    toss=data.toss_decision.value_counts().reset_index()
    toss.columns=["Decision","Count"]
    fig2=px.pie(
        toss,
        names="Decision",
        values="Count",
        hole=.45,
        title="Toss Decision"
    )
    st.plotly_chart(fig2,use_container_width=True)

with col2:
    stage=data.stage.value_counts().reset_index()
    stage.columns=["Stage","Matches"]
    fig3=px.bar(stage,x="Stage",y="Matches",color="Matches",text="Matches")
    st.plotly_chart(fig3,use_container_width=True)

st.subheader("🔥 Top Scores")

top=(data[["top_scorer","highscore"]]
     .drop_duplicates()
     .sort_values("highscore",ascending=False)
     .head(10))

fig4=px.bar(top,x="top_scorer",y="highscore",color="highscore",text="highscore")
st.plotly_chart(fig4,use_container_width=True)

with st.expander("Dataset Preview"):
    st.dataframe(data,use_container_width=True,hide_index=True)

csv=data.to_csv(index=False)

st.download_button(
    "Download Filtered Dataset",
    csv,
    "IPL_Filtered_Data.csv",
    "text/csv"
)

st.markdown("---")
st.markdown(
"<center><b>Developed by Kamlesh Nayak</b><br>"
"Python • Pandas • Plotly • Streamlit</center>",
unsafe_allow_html=True
)
