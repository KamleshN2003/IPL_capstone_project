import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Venue Analysis",
    page_icon="🏟",
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
# Sidebar
# --------------------------------------------------
st.sidebar.header("🏟 Venue Filter")

venues = sorted(df["venue"].dropna().unique())

selected_venue = st.sidebar.selectbox(
    "Select Venue",
    ["All Venues"] + venues
)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------
filtered_df = df.copy()

if selected_venue != "All Venues":
    filtered_df = filtered_df[
        filtered_df["venue"] == selected_venue
    ]

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("🏟 Venue Analysis")

st.write(
    "Analyze IPL matches played across different venues."
)

st.divider()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
matches = filtered_df.shape[0]

venues_count = filtered_df["venue"].nunique()

highest_score = filtered_df["first_ings_score"].max()

avg_score = round(filtered_df["first_ings_score"].mean(), 2)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Matches", matches)
c2.metric("Venues", venues_count)
c3.metric("Highest Score", highest_score)
c4.metric("Average Score", avg_score)

st.divider()

# --------------------------------------------------
# Matches Per Venue
# --------------------------------------------------
st.subheader("📊 Matches Played at Each Venue")

venue_matches = (
    df["venue"]
    .value_counts()
    .reset_index()
)

venue_matches.columns = ["Venue", "Matches"]

fig1 = px.bar(
    venue_matches,
    x="Venue",
    y="Matches",
    color="Matches",
    text="Matches",
    title="Matches Played at Each Venue"
)

st.plotly_chart(fig1, use_container_width=True)

st.divider()

# --------------------------------------------------
# Venue Winners
# --------------------------------------------------
st.subheader("🏆 Match Winners at Selected Venue")

winner_count = (
    filtered_df["match_winner"]
    .value_counts()
    .reset_index()
)

winner_count.columns = ["Team", "Wins"]

fig2 = px.bar(
    winner_count,
    x="Team",
    y="Wins",
    color="Wins",
    text="Wins",
    title="Venue-wise Match Winners"
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --------------------------------------------------
# Toss Decision
# --------------------------------------------------
st.subheader("🪙 Toss Decision")

decision = (
    filtered_df["toss_decision"]
    .value_counts()
    .reset_index()
)

decision.columns = ["Decision", "Count"]

fig3 = px.pie(
    decision,
    names="Decision",
    values="Count",
    title="Bat vs Field"
)

st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --------------------------------------------------
# Average First Innings Score
# --------------------------------------------------
st.subheader("🔥 Average First Innings Score")

avg_scores = (
    df.groupby("venue")["first_ings_score"]
    .mean()
    .reset_index()
)

avg_scores.columns = ["Venue", "Average Score"]

fig4 = px.bar(
    avg_scores,
    x="Venue",
    y="Average Score",
    color="Average Score",
    text="Average Score",
    title="Average First Innings Score by Venue"
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

# --------------------------------------------------
# Match Details
# --------------------------------------------------
st.subheader("📋 Venue Match Details")

columns = [
    "date",
    "team1",
    "team2",
    "venue",
    "first_ings_score",
    "match_winner",
    "won_by"
]

available_columns = [col for col in columns if col in filtered_df.columns]

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Download CSV
# --------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Venue Data",
    csv,
    file_name="venue_analysis.csv",
    mime="text/csv"
)

st.success("✅ Venue Analysis Loaded Successfully")