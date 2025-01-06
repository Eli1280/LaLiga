import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Charger les fichiers CSV
home_table_df = pd.read_csv('Laliga_table_home_2023_24.csv')
away_table_df = pd.read_csv('Laliga_table_away_2023_24.csv')
team_goals_df = pd.read_csv('data/team_goals_per_match.csv')
team_ratings_df = pd.read_csv('team_ratings.csv')
team_tackles_df = pd.read_csv('won_tackle_team.csv', sep=',')
player_goals_df = pd.read_csv('player_goals_per_90.csv', sep=',')

# Charger les statistiques des joueurs
accurate_passes_df = pd.read_csv('data/player_accurate_passes.csv')
big_chances_created_df = pd.read_csv('data/player_big_chances_created.csv')
interceptions_df = pd.read_csv('data/player_interceptions.csv')
contests_won_df = pd.read_csv('data/player_contests_won.csv')

# Renommer les colonnes des DataFrames des joueurs
accurate_passes_df.columns = ['Rank', 'Player', 'Team', 'Pass Success (%)', 'Total Passes', 'Minutes', 'Matches', 'Country']
big_chances_created_df.columns = ['Rank', 'Player', 'Team', 'Chances Created', 'Goals', 'Minutes', 'Matches', 'Country']
interceptions_df.columns = ['Rank', 'Player', 'Team', 'Goals', 'Interceptions', 'Matches', 'Minutes', 'Country']
contests_won_df.columns = ['Rank', 'Player', 'Team', 'Goals', 'Dribble Success(%)', 'Minutes', 'Matches', 'Country']
player_goals_df.columns = ['Rank', 'Player', 'Team', 'Goals', 'Total Goals', 'Minutes', 'Matches', 'Country']

# Sélectionner les colonnes nécessaires pour l'analyse
player_goals_df = player_goals_df[['Player', 'Total Goals']]
accurate_passes_df = accurate_passes_df[['Player', 'Pass Success (%)']]
big_chances_created_df = big_chances_created_df[['Player', 'Chances Created']]
interceptions_df = interceptions_df[['Player', 'Interceptions']]
contests_won_df = contests_won_df[['Player', 'Dribble Success(%)']]

# Fusionner les DataFrames sur la colonne 'Player'
player_stats_df = accurate_passes_df.merge(big_chances_created_df, on='Player', how='right')
player_stats_df = player_stats_df.merge(interceptions_df, on='Player', how='right')
player_stats_df = player_stats_df.merge(contests_won_df, on='Player', how='right')
player_stats_df = player_stats_df.merge(player_goals_df, on='Player', how='right')

# Application Streamlit
st.title("LaLiga Dashboard 2023/24")

# Sidebar de navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Team Statistics", "Player Statistics"])

# Page: Vue d'ensemble
if page == "Overview":
    st.header("Overview of LaLiga 2023/24")
    st.write("Comparison of Home and Away Performance")

    home_table_df['location'] = 'Home'
    away_table_df['location'] = 'Away'

    # Combinaison des tableaux de maison et extérieur
    combined_df = pd.concat([home_table_df[['name', 'pts', 'wins', 'draws', 'losses', 'goalConDiff', 'location']],
                             away_table_df[['name', 'pts', 'wins', 'draws', 'losses', 'goalConDiff', 'location']]])

    fig = px.bar(combined_df, x='name', y='pts', color='location', 
                 title='Points Comparison: Home vs Away', labels={'pts': 'Points', 'name': 'Team'})
    st.plotly_chart(fig)

# Page: Statistiques des équipes
elif page == "Team Statistics":
    st.header("Team Statistics")
    st.write("Explore team performance in different metrics.")

    # Graphiques pour les statistiques des équipes
    st.subheader("Goals Per Match")
    fig_goals = px.bar(team_goals_df, x='Team', y='Goals per Match', title='Goals per Match by Team')
    st.plotly_chart(fig_goals)

    st.subheader("Team Ratings")
    fig_ratings = px.bar(team_ratings_df, x='Team', y='FotMob Team Rating', title='Team Ratings')
    st.plotly_chart(fig_ratings)

    st.subheader("Tackles Won")
    fig_tackles = px.bar(team_tackles_df, x='Team', y='Successful Tackles per Match', title='Tackles Won by Team')
    st.plotly_chart(fig_tackles)

# Page: Statistiques des joueurs
elif page == "Player Statistics":
    st.header("Player Statistics")
    st.write("Compare performance of players in LaLiga.")

    # Sélection des joueurs à comparer
    selected_players = st.multiselect(
        "Select players to compare:",
        options=player_stats_df['Player'].unique(),
        default=player_stats_df['Player'].unique()[:2]
    )

    if selected_players:
        # Filtrer les données pour les joueurs sélectionnés
        filtered_stats = player_stats_df[player_stats_df['Player'].isin(selected_players)]
        st.subheader("Player Statistics Table")
        player_stats_display = filtered_stats[['Player', 'Pass Success (%)', 'Chances Created', 'Interceptions', 'Dribble Success(%)', 'Total Goals']]
        st.dataframe(player_stats_display, use_container_width=True)

        # Fonction pour standardiser les colonnes
        def standardize_column(column, min_val=20, max_val=80):
            col_max = column.max()
            col_min = column.min()
            normalized_column = (column - col_min) / (col_max - col_min)
            return normalized_column * (max_val - min_val) + min_val

        # Normaliser les colonnes
        columns_to_standardize = ['Pass Success (%)', 'Chances Created', 'Interceptions', 'Dribble Success(%)', 'Total Goals']
        for col in columns_to_standardize:
            player_stats_df[col] = standardize_column(player_stats_df[col])

        # Graphique radar pour la comparaison détaillée
        st.subheader("Radar Chart Comparison")
        radar_categories = ['Pass Success (%)', 'Chances Created', 'Interceptions', 'Dribble Success(%)', 'Total Goals']

        # Créer le graphique radar
        fig_radar = go.Figure()
        for player in selected_players:
            player_data = player_stats_df[player_stats_df['Player'] == player].iloc[0]
            fig_radar.add_trace(go.Scatterpolar(
                r=[player_data[stat] for stat in radar_categories],
                theta=radar_categories,
                fill='toself',
                name=player
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=False), angularaxis=dict(visible=True)),
            showlegend=True
        )
        st.plotly_chart(fig_radar)

    else:
        st.write("Select players to see their comparison.")
