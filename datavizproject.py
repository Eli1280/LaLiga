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
team_goals_df = pd.read_csv('data/team_goals_per_match.csv')
team_ratings_df = pd.read_csv('team_ratings.csv')
team_tackles_df = pd.read_csv('won_tackle_team.csv', sep=',')
player_goals_df = pd.read_csv('player_goals_per_90.csv', sep=',')

# Load additional player stats for radar chart
accurate_passes_df = pd.read_csv('data/player_accurate_passes.csv')
big_chances_created_df = pd.read_csv('data/player_big_chances_created.csv')
interceptions_df = pd.read_csv('data/player_interceptions.csv')
contests_won_df = pd.read_csv('data/player_contests_won.csv')

# Renommer les colonnes si nécessaire et sélectionner les données importantes
accurate_passes_df.columns = ['Rank', 'Player', 'Team', 'Pass Success (%)', 'Total Passes', 'Minutes', 'Matches', 'Country']
big_chances_created_df.columns = ['Rank', 'Player', 'Team', 'Big Chances Created', 'Goals', 'Minutes', 'Matches', 'Country']
interceptions_df.columns = ['Rank', 'Player', 'Team','Goals', 'Interceptions', 'Matches', 'Country']
contests_won_df.columns = ['Rank', 'Player', 'Team', 'Goals', 'Dribble Success Rate (%)',  'Minutes', 'Matches', 'Country']
player_goals_df.columns = ['Rank', 'Player', 'Team', 'Goals', 'Total Goals', 'Matches', 'Country']

# Sélectionner uniquement les colonnes nécessaires pour chaque fichier
player_goals_df = player_goals_df[['Player', 'Total Goals']]
accurate_passes_df = accurate_passes_df[['Player', 'Pass Success (%)']]
big_chances_created_df = big_chances_created_df[['Player', 'Big Chances Created']]
interceptions_df = interceptions_df[['Player', 'Interceptions']]
contests_won_df = contests_won_df[['Player', 'Dribble Success Rate (%)']]

# Fusionner les DataFrames sur la colonne 'Player'
player_stats_df = accurate_passes_df.merge(big_chances_created_df, on='Player', how='right')
player_stats_df = player_stats_df.merge(interceptions_df, on='Player', how='right')
player_stats_df = player_stats_df.merge(contests_won_df, on='Player', how='right')
player_stats_df = player_stats_df.merge(player_goals_df, on='Player', how='right')

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
        options=player_stats_df['Player'].unique(),
        default=player_stats_df['Player'].unique()[:2]  # Pre-select the first two players
    )

    if selected_players:
        
        # Filter data for selected players
        filtered_stats = player_stats_df[player_stats_df['Player'].isin(selected_players)]
        st.subheader("Player Statistics Table")
        player_stats_display = filtered_stats[['Player', 'Pass Success (%)', 'Big Chances Created', 'Interceptions', 'Dribble Success Rate (%)','Total Goals']]
        st.dataframe(player_stats_display)

        # Radar chart for detailed comparison
        st.subheader("Radar Chart Comparison")

        # Define the categories for the radar chart based on imported CSVs
        radar_categories = [
            'Pass Success (%)',  # From player_accurate_passes.csv
            'Big Chances Created',  # From player_big_chances_created.csv
            'Interceptions',  # From player_interceptions.csv
            'Dribble Success Rate (%)',  # From player_contests_won.csv
            'Total Goals'
        ]


        scales = {
            'Pass Success (%)': [0, 100],  # Pourcentage, donc de 0 à 100
            'Big Chances Created': [0, filtered_stats['Big Chances Created'].max() + 1],
            'Interceptions': [0, filtered_stats['Interceptions'].max() + 1],
            'Dribble Success Rate (%)': [0, 100]
        }

        # Créer le radar chart
        fig_radar = go.Figure()

        for player in selected_players:
            player_data = filtered_stats[filtered_stats['Player'] == player].iloc[0]
            fig_radar.add_trace(go.Scatterpolar(
                r=[player_data[stat] for stat in radar_categories],
                theta=radar_categories,
                fill='toself',
                name=player
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=False,  # Ne pas afficher les valeurs sur l'axe radial
                ),
                angularaxis=dict(
                    visible=True  # Afficher les labels des catégories
                ),
            ),
            showlegend=True
        )
        # Afficher le graphique radar dans Streamlit
        st.plotly_chart(fig_radar)
    else:
        st.write("Select players to see their comparison.")
