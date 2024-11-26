import streamlit as st
import pandas as pd
import plotly.express as px

# Sample data (replace this with your real data)
teams = ["Tom Brady Fan Club",
         "Danish Lions",
         "OG of OG's",
         "Mr.Universe",
         "Manning's Bagels",
         "Maine Lobster rolls",
         "Ludwig's Giants",
         "The Rat Pack",
         "The King in the North",
         "Team eL",
         "Watson's Massage Parlor",
         "Harry's Genius Team"]

qual_probabilities = [0.88,
                      1.0,
                      1.0,
                      0.0,
                      0.09,
                      0.0,
                      0.96,
                      0.0,
                      0.0,
                      0.98,
                      0.40,
                      0.60]

scenarios_count = [56,
                   64,
                   64,
                   0,
                   8,
                   0,
                   61,
                   0,
                   0,
                   63,
                   24,
                   36]

most_likely_scenarios = [
    [
        # For Tom Brady Fan Club
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: The King in the North wins against Harry's Genius Team"

    ],
    [
        # For Danish Lions
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: The King in the North wins against Harry's Genius Team"
    ],
    [
        # For OG of OG's
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: The King in the North wins against Harry's Genius Team"
    ],
    [
        # For Mr.Universe
        "No qualifying scenarios"
    ],
    [
        # For Manning's Bagels
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Manning's Bagels wins against Danish Lions",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Maine lobster rolls wins against Watson's Massage Parlor",
        "week 13: The King in the North wins against Harry's Genius Team"
    ],
    [
        # For Maine lobster rolls
        "No qualifying scenarios"
    ],
    [
        # For Ludwig's Giants
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: The King in the North wins against Harry's Genius Team"
    ],
    [
        # For The Rat Pack
        "No qualifying scenarios"
    ],
    [
        # For The King in the North
        "No qualifying scenarios"
    ],
    [
        # For Team eL
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: The King in the North wins against Harry's Genius Team"
    ],
    [
        # For Watson's Massage Parlor
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: Harry's Genius Team wins against The King in the North"
    ],
    [
        # For Harry's Genius Team
        "week 13: Tom Brady Fan Club wins against The Rat Pack",
        "week 13: Team eL wins against The OG of OG's",
        "week 13: Danish Lions wins against Manning's Bagels",
        "week 13: Ludwig's Giants wins against Mr.Universe",
        "week 13: Watson's Massage Parlor wins against Maine lobster rolls",
        "week 13: Harry's Genius Team wins against The King in the North"
    ]
]

# Dashboard Layout
st.title("Fantasy Football Playoff Dashboard")
st.sidebar.header("Team Selection")
selected_team = st.sidebar.selectbox("Select a Team:", teams)

# Display Team Statistics
team_idx = teams.index(selected_team)
st.header(f"Playoff Scenarios for {selected_team}")
st.subheader(f"Total Qualification Probability: {qual_probabilities[team_idx]:.2%}")
st.subheader(f"Number of Qualifying Scenarios: {scenarios_count[team_idx]}")

# Show Most Likely Scenario
st.markdown("### Most Likely Qualifying Scenario:")
for line in most_likely_scenarios[team_idx]:
    st.markdown(f"- {line}")

# Probability Bar Chart
st.markdown("### Qualification Probabilities for All Teams")
prob_df = pd.DataFrame({"Team": teams, "Qualification Probability": qual_probabilities})
fig = px.bar(prob_df, x="Team", y="Qualification Probability", text="Qualification Probability",
             color="Qualification Probability", color_continuous_scale="Blues")
st.plotly_chart(fig)

# Scenarios Table
st.markdown("### Detailed Scenarios for All Teams")
scenarios_df = pd.DataFrame({
    "Team": teams,
    "Qualification Probability (%)": [p * 100 for p in qual_probabilities],
    "Number of Scenarios": scenarios_count,
})
st.dataframe(scenarios_df)

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit.")
