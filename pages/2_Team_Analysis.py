import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Team Analysis",
    page_icon="🏆",
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
st.sidebar.header("🏏 Team Filter")

teams = sorted(
    list(
        pd.unique(
            pd.concat([df["team1"], df["team2"]])
        )
    )
)

selected_team = st.sidebar.selectbox(
    "Select Team",
    teams
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------
team_df = df[
    (df["team1"] == selected_team) |
    (df["team2"] == selected_team)
]

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title(f"🏆 {selected_team} Analysis")

st.write("Explore team performance across the IPL 2022 season.")

st.divider()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
matches = len(team_df)

wins = len(team_df[team_df["match_winner"] == selected_team])

losses = matches - wins

win_percentage = round((wins / matches) * 100, 2) if matches else 0

highest_score = team_df["first_ings_score"].max()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Matches", matches)
c2.metric("Wins", wins)
c3.metric("Losses", losses)
c4.metric("Win %", f"{win_percentage}%")

st.divider()

# --------------------------------------------------
# Overall Team Wins
# --------------------------------------------------
st.subheader("🏆 Overall Team Wins")

team_wins = (
    df["match_winner"]
    .value_counts()
    .reset_index()
)

team_wins.columns = ["Team", "Wins"]

fig = px.bar(
    team_wins,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Matches Won by Each Team"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Toss Decision
# --------------------------------------------------
left, right = st.columns(2)

with left:

    st.subheader("🪙 Toss Decision")

    toss = (
        team_df["toss_decision"]
        .value_counts()
        .reset_index()
    )

    toss.columns = ["Decision", "Count"]

    fig2 = px.pie(
        toss,
        names="Decision",
        values="Count",
        title="Bat vs Field"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:

    st.subheader("🏟 Matches by Stage")

    stage = (
        team_df["stage"]
        .value_counts()
        .reset_index()
    )

    stage.columns = ["Stage", "Matches"]

    fig3 = px.bar(
        stage,
        x="Stage",
        y="Matches",
        color="Matches",
        text="Matches"
    )

    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --------------------------------------------------
# First Innings Score
# --------------------------------------------------
st.subheader("🔥 First Innings Scores")

fig4 = px.histogram(
    team_df,
    x="first_ings_score",
    nbins=10,
    color_discrete_sequence=["orange"]
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --------------------------------------------------
# Match History
# --------------------------------------------------
st.subheader("📋 Match History")

columns = [
    "date",
    "team1",
    "team2",
    "venue",
    "stage",
    "match_winner",
    "margin"
]

available_columns = [c for c in columns if c in team_df.columns]

st.dataframe(
    team_df[available_columns],
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Download CSV
# --------------------------------------------------
csv = team_df.to_csv(index=False)

st.download_button(
    "⬇ Download Team Data",
    csv,
    file_name=f"{selected_team}_analysis.csv",
    mime="text/csv"
)

st.success("✅ Team Analysis Loaded Successfully")