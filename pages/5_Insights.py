import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="IPL Insights",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("IPL.csv")

df = load_data()

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📈 IPL 2022 Business Insights")

st.write(
    """
    This page summarizes the key findings from the IPL 2022 dataset.
    These insights help understand team performance, player impact,
    venue statistics, and match trends.
    """
)

st.divider()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
best_team = df["match_winner"].value_counts().idxmax()
team_wins = df["match_winner"].value_counts().max()

best_player = df["player_of_the_match"].value_counts().idxmax()
player_awards = df["player_of_the_match"].value_counts().max()

best_venue = df["venue"].value_counts().idxmax()

highest_score = df["first_ings_score"].max()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏆 Best Team", best_team)
c2.metric("⭐ Best Player", best_player)
c3.metric("🏟 Most Used Venue", best_venue)
c4.metric("🔥 Highest Score", highest_score)

st.divider()

# --------------------------------------------------
# Team Wins Chart
# --------------------------------------------------
st.subheader("🏆 Team Performance")

team_df = (
    df["match_winner"]
    .value_counts()
    .reset_index()
)

team_df.columns = ["Team", "Wins"]

fig = px.bar(
    team_df,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Matches Won by Each Team"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Player Awards
# --------------------------------------------------
st.subheader("⭐ Player of the Match Awards")

player_df = (
    df["player_of_the_match"]
    .value_counts()
    .head(10)
    .reset_index()
)

player_df.columns = ["Player", "Awards"]

fig2 = px.bar(
    player_df,
    x="Player",
    y="Awards",
    color="Awards",
    text="Awards",
    title="Top 10 Players of the Match"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --------------------------------------------------
# Toss Decision
# --------------------------------------------------
st.subheader("🪙 Toss Decision Distribution")

fig3 = px.pie(
    df,
    names="toss_decision",
    title="Bat vs Field Decision"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --------------------------------------------------
# Venue Analysis
# --------------------------------------------------
st.subheader("🏟 Matches Played by Venue")

venue_df = (
    df["venue"]
    .value_counts()
    .reset_index()
)

venue_df.columns = ["Venue", "Matches"]

fig4 = px.bar(
    venue_df,
    x="Venue",
    y="Matches",
    color="Matches",
    text="Matches",
    title="Venue-wise Matches"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --------------------------------------------------
# Key Insights
# --------------------------------------------------
st.subheader("💡 Key Insights")

st.success(f"🏆 {best_team} won the highest number of matches ({team_wins} wins).")

st.success(f"⭐ {best_player} received the most Player of the Match awards ({player_awards}).")

st.success(f"🏟 {best_venue} hosted the highest number of matches.")

st.success(f"🔥 Highest first innings score recorded: {highest_score}.")

st.success(
    f"📊 Average first innings score: {round(df['first_ings_score'].mean(), 2)}."
)

st.divider()

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------
st.subheader("📄 Executive Summary")

st.info("""
• The dataset provides insights into IPL 2022 matches.

• Team performance is evaluated based on total wins.

• Player performance is measured using Player of the Match awards.

• Venue analysis identifies stadiums hosting the most matches.

• Toss decision analysis shows the preference between batting and fielding first.

• Overall, this dashboard helps users explore IPL trends using interactive visualizations.
""")

st.divider()

# --------------------------------------------------
# Download Dataset
# --------------------------------------------------
csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Complete Dataset",
    csv,
    file_name="IPL_2022_Data.csv",
    mime="text/csv"
)

st.success("✅ Insights Dashboard Loaded Successfully")