import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# --------------------------------------------------
# Page Config
# --------------------------------------------------
st.set_page_config(
    page_title="ML Predictor",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("IPL.csv")

df = load_data()

st.title("🤖 First Innings Score Predictor")
st.write("Predict the expected first innings score using Machine Learning.")

# --------------------------------------------------
# Features & Target
# --------------------------------------------------
features = [
    "team1",
    "team2",
    "venue",
    "toss_winner",
    "toss_decision",
    "stage"
]

target = "first_ings_score"

X = df[features]
y = df[target]

# --------------------------------------------------
# Pipeline
# --------------------------------------------------
preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            features
        )
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(
            n_estimators=200,
            random_state=42
        ))
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model.fit(X_train, y_train)

pred = model.predict(X_test)

r2 = r2_score(y_test, pred)
mae = mean_absolute_error(y_test, pred)

st.success("✅ Model Trained Successfully")

# --------------------------------------------------
# Metrics
# --------------------------------------------------
c1, c2 = st.columns(2)

c1.metric("R² Score", round(r2, 2))
c2.metric("MAE", round(mae, 2))

st.divider()

# --------------------------------------------------
# Prediction Form
# --------------------------------------------------
st.subheader("Predict Score")

team1 = st.selectbox("Batting Team", sorted(df["team1"].unique()))
team2 = st.selectbox("Bowling Team", sorted(df["team2"].unique()))
venue = st.selectbox("Venue", sorted(df["venue"].unique()))
toss = st.selectbox("Toss Winner", sorted(df["toss_winner"].unique()))
decision = st.selectbox("Toss Decision", sorted(df["toss_decision"].unique()))
stage = st.selectbox("Stage", sorted(df["stage"].unique()))

if st.button("Predict Score"):

    sample = pd.DataFrame({
        "team1":[team1],
        "team2":[team2],
        "venue":[venue],
        "toss_winner":[toss],
        "toss_decision":[decision],
        "stage":[stage]
    })

    prediction = model.predict(sample)[0]

    st.success(
        f"🏏 Predicted First Innings Score: **{round(prediction)} runs**"
    )

st.divider()

# --------------------------------------------------
# Model Information
# --------------------------------------------------
st.subheader("Model Details")

st.write("""
**Algorithm Used:** Random Forest Regressor

**Input Features**
- Team 1
- Team 2
- Venue
- Toss Winner
- Toss Decision
- Match Stage

**Target**
- First Innings Score
""")