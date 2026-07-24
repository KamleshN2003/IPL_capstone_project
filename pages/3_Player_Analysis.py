import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Player Analysis",
    page_icon="⭐",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("IPL.csv")

df = load_data()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("⭐ Player Filter")

players = sorted(df["player_of_the_match"].dropna().unique())

selected_player = st.sidebar.selectbox(
    "Select Player",
    ["All Players"] + players
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------
filtered_df = df.copy()

if selected_player != "All Players":
    filtered_df = filtered_df[
        filtered_df["player_of_the_match"] == selected_player
    ]

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("⭐ Player Analysis")

st.write("Analyze Player of the Match awards and batting performances.")

st.divider()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
total_awards = filtered_df["player_of_the_match"].count()

highest_score = filtered_df["highscore"].max()

average_score = round(filtered_df["highscore"].mean(), 2)

unique_players = filtered_df["player_of_the_match"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Awards", total_awards)
c2.metric("Highest Score", highest_score)
c3.metric("Average Score", average_score)
c4.metric("Players", unique_players)

st.divider()

# --------------------------------------------------
# Top Player of Match Winners
# --------------------------------------------------
st.subheader("🏆 Top 10 Player of the Match Winners")

pom = (
    df["player_of_the_match"]
    .value_counts()
    .head(10)
    .reset_index()
)

pom.columns = ["Player", "Awards"]

fig = px.bar(
    pom,
    x="Player",
    y="Awards",
    color="Awards",
    text="Awards",
    title="Top Player of the Match Winners"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Highest Individual Scores
# --------------------------------------------------
st.subheader("🔥 Highest Individual Scores")

top_scores = (
    df[["top_scorer", "highscore"]]
    .drop_duplicates()
    .sort_values(
        "highscore",
        ascending=False
    )
    .head(10)
)

fig2 = px.bar(
    top_scores,
    x="top_scorer",
    y="highscore",
    color="highscore",
    text="highscore",
    title="Top 10 Highest Individual Scores"
)

fig2.update_layout(
    xaxis_title="Player",
    yaxis_title="Runs"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --------------------------------------------------
# Player Statistics
# --------------------------------------------------
st.subheader("📋 Player Statistics")

stats = filtered_df[
    [
        "player_of_the_match",
        "top_scorer",
        "highscore"
    ]
]

st.dataframe(
    stats,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Download Button
# --------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇ Download Player Data",
    data=csv,
    file_name="player_analysis.csv",
    mime="text/csv"
)

st.success("✅ Player Analysis Loaded Successfully")