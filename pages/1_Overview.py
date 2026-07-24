import streamlit as st
import pandas as pd

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="Overview",
    page_icon="📊",
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
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("📊 Filters")

teams = sorted(
    list(
        pd.unique(
            pd.concat([df["team1"], df["team2"]])
        )
    )
)

selected_team = st.sidebar.selectbox(
    "Select Team",
    ["All Teams"] + teams
)

venues = sorted(df["venue"].dropna().unique())

selected_venue = st.sidebar.selectbox(
    "Select Venue",
    ["All Venues"] + list(venues)
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if selected_team != "All Teams":
    filtered_df = filtered_df[
        (filtered_df["team1"] == selected_team)
        |
        (filtered_df["team2"] == selected_team)
    ]

if selected_venue != "All Venues":
    filtered_df = filtered_df[
        filtered_df["venue"] == selected_venue
    ]

# --------------------------------------------------
# Title
# --------------------------------------------------
st.title("📊 Dataset Overview")

st.write(
    "Explore IPL 2022 dataset using interactive filters."
)

st.divider()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
matches = filtered_df.shape[0]

teams_count = len(
    pd.unique(
        pd.concat(
            [
                filtered_df["team1"],
                filtered_df["team2"]
            ]
        )
    )
)

venues_count = filtered_df["venue"].nunique()

highest_score = filtered_df["first_ings_score"].max()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Matches", matches)

c2.metric("👥 Teams", teams_count)

c3.metric("🏟 Venues", venues_count)

c4.metric("🔥 Highest Score", highest_score)

st.divider()

# --------------------------------------------------
# Dataset Preview
# --------------------------------------------------
st.subheader("📋 Dataset Preview")

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Dataset Shape
# --------------------------------------------------
left, right = st.columns(2)

with left:

    st.subheader("📐 Dataset Shape")

    st.info(f"Rows : {filtered_df.shape[0]}")

    st.info(f"Columns : {filtered_df.shape[1]}")

with right:

    st.subheader("❌ Missing Values")

    missing = filtered_df.isnull().sum()

    st.dataframe(
        missing,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# Data Types
# --------------------------------------------------
st.subheader("📝 Column Information")

column_info = pd.DataFrame(
    {
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str)
    }
)

st.dataframe(
    column_info,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Statistical Summary
# --------------------------------------------------
st.subheader("📈 Statistical Summary")

st.dataframe(
    filtered_df.describe(),
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# First Innings Score Distribution
# --------------------------------------------------
st.subheader("📊 First Innings Score Distribution")

st.bar_chart(
    filtered_df["first_ings_score"]
)

st.divider()

# --------------------------------------------------
# Download
# --------------------------------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Dataset",
    csv,
    file_name="IPL_Filtered_Data.csv",
    mime="text/csv"
)

st.success("✅ Overview Loaded Successfully")