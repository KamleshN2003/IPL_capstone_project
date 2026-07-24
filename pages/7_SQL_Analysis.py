import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="SQL Analysis",
    page_icon="🗄️",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("IPL.csv")

df = load_data()

st.title("🗄️ SQL Analysis Dashboard")
st.write("SQL-style analytics using the IPL 2022 dataset.")

st.divider()

# ==================================================
# 1. Team Wins
# ==================================================
st.subheader("1️⃣ Top Winning Teams")

st.code("""
SELECT match_winner, COUNT(*) AS wins
FROM IPL
GROUP BY match_winner
ORDER BY wins DESC;
""", language="sql")

wins = (
    df["match_winner"]
    .value_counts()
    .reset_index()
)

wins.columns = ["Team", "Wins"]

fig = px.bar(
    wins,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Team Wins"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(wins, use_container_width=True)

st.divider()

# ==================================================
# 2. Matches Played
# ==================================================
st.subheader("2️⃣ Matches Played by Each Team")

st.code("""
SELECT team_name,
COUNT(*) AS matches
FROM (
SELECT team1 AS team_name FROM IPL
UNION ALL
SELECT team2 FROM IPL
)
GROUP BY team_name;
""", language="sql")

teams = pd.concat([df["team1"], df["team2"]])

matches = (
    teams.value_counts()
    .reset_index()
)

matches.columns = ["Team", "Matches"]

fig = px.bar(
    matches,
    x="Team",
    y="Matches",
    color="Matches",
    text="Matches"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================================================
# 3. Top Scorers
# ==================================================
st.subheader("3️⃣ Most Frequent Top Scorers")

st.code("""
SELECT top_scorer,
COUNT(*) AS appearances
FROM IPL
GROUP BY top_scorer
ORDER BY appearances DESC;
""", language="sql")

scorers = (
    df["top_scorer"]
    .value_counts()
    .head(10)
    .reset_index()
)

scorers.columns = ["Player", "Appearances"]

fig = px.bar(
    scorers,
    x="Player",
    y="Appearances",
    color="Appearances",
    text="Appearances"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================================================
# 4. Player of the Match
# ==================================================
st.subheader("4️⃣ Player of the Match Awards")

st.code("""
SELECT player_of_the_match,
COUNT(*) AS awards
FROM IPL
GROUP BY player_of_the_match
ORDER BY awards DESC;
""", language="sql")

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
    text="Awards"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================================================
# 5. Venue Usage
# ==================================================
st.subheader("5️⃣ Matches Played at Each Venue")

st.code("""
SELECT venue,
COUNT(*) AS matches
FROM IPL
GROUP BY venue
ORDER BY matches DESC;
""", language="sql")

venue = (
    df["venue"]
    .value_counts()
    .reset_index()
)

venue.columns = ["Venue", "Matches"]

fig = px.bar(
    venue,
    x="Venue",
    y="Matches",
    color="Matches",
    text="Matches"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================================================
# 6. Toss Decision
# ==================================================
st.subheader("6️⃣ Toss Decision Distribution")

st.code("""
SELECT toss_decision,
COUNT(*) AS total
FROM IPL
GROUP BY toss_decision;
""", language="sql")

toss = (
    df["toss_decision"]
    .value_counts()
    .reset_index()
)

toss.columns = ["Decision", "Count"]

fig = px.pie(
    toss,
    names="Decision",
    values="Count",
    hole=0.45,
    title="Bat vs Field"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ==================================================
# 7. Highest First Innings Scores
# ==================================================
st.subheader("7️⃣ Highest First Innings Scores")

st.code("""
SELECT team1,
first_ings_score
FROM IPL
ORDER BY first_ings_score DESC
LIMIT 10;
""", language="sql")

top_scores = (
    df[["team1", "first_ings_score"]]
    .sort_values("first_ings_score", ascending=False)
    .head(10)
)

fig = px.bar(
    top_scores,
    x="team1",
    y="first_ings_score",
    color="first_ings_score",
    text="first_ings_score"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(top_scores, use_container_width=True)

st.divider()

# ==================================================
# Download
# ==================================================
csv = df.to_csv(index=False)

st.download_button(
    "⬇ Download Dataset",
    csv,
    "IPL_SQL_Data.csv",
    "text/csv"
)

st.success("✅ SQL Analysis Loaded Successfully")