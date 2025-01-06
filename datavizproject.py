import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dataframes import load_dataframes
import os



# Load the CSV files
home_table_df = pd.read_csv('Laliga_table_home_2023_24.csv')
away_table_df = pd.read_csv('Laliga_table_away_2023_24.csv')
overall_table_df = pd.read_csv('Laliga_table_2023_24.csv')
team_goals_df = pd.read_csv('team_goals_per_match.csv')
team_ratings_df = pd.read_csv('team_ratings.csv')
team_tackles_df = pd.read_csv('won_tackle_team.csv')
player_goals_df = pd.read_csv('player_goals_per_90.csv')


# Streamlit app
st.title("LaLiga Dashboard 2023/24")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Team Statistics", "Player Statistics"])

# Page: Overview
if page == "Overview":
    st.header("Overview of LaLiga 2023/24")
    st.write("Comparison of Home and Away Performance")

    home_table_df['location'] = 'Home'
    away_table_df['location'] = 'Away'

    combined_df = pd.concat([
        home_table_df[['name', 'pts', 'wins', 'draws', 'losses', 'goalConDiff', 'location']],
        away_table_df[['name', 'pts', 'wins', 'draws', 'losses', 'goalConDiff', 'location']]
    ])

    fig = px.bar(combined_df, x='name', y='pts', color='location',
                 title='Points Comparison: Home vs Away vs Overall',
                 labels={'pts': 'Points', 'name': 'Team'},
                 category_orders={'location': ['Home', 'Away', 'Overall']})
    st.plotly_chart(fig)

# Page: Team Statistics
elif page == "Team Statistics":
    st.header("Team Statistics")
    st.write("Explore team performance in different metrics.")

    # Goals per match
    st.subheader("Goals Per Match")
    fig_goals = px.bar(team_goals_df, x='Team', y='Goals per Match', title='Goals per Match by Team')
    st.plotly_chart(fig_goals)

    # Team ratings
    st.subheader("Team Ratings")
    fig_ratings = px.bar(team_ratings_df, x='Team', y='FotMob Team Rating', title='Team Ratings')
    st.plotly_chart(fig_ratings)

    # Tackles won
    st.subheader("Tackles Won")
    fig_tackles = px.bar(team_tackles_df, x='Team', y='Successful Tackles per Match', title='Tackles Won by Team')
    st.plotly_chart(fig_tackles)

# Page: Player Statistics
elif page == "Player Statistics":
    st.header("Player Statistics")
    st.write("Compare performance of players in LaLiga.")

    # Select players to compare
    selected_players = st.multiselect(
        "Select players to compare:",
        options=player_goals_df['Player'].unique(),
        default=player_goals_df['Player'].unique()[:2]  # Pre-select the first two players
    )

    if selected_players:
        filtered_df = player_goals_df[player_goals_df['Player'].isin(selected_players)]
        fig_players = px.bar(filtered_df, x='Player', y='Goals per 90',
                             title='Goals Per 90 Minutes Comparison',
                             labels={'Goals per 90': 'Goals per 90 Minutes', 'Player': 'Player'})
        st.plotly_chart(fig_players)
    else:
        st.write("Select players to see their comparison.")
