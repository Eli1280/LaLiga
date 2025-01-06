import plotly.express as px
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from dataframes import load_dataframes
import os

folder_path = 'data/'
csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Charger les CSV et les filtrer pour ceux contenant 'player' dans le nom
player_csvs = []
for file in csv_files:
    if 'player' in file.lower():  # Filtre par nom de fichier
        df = pd.read_csv(os.path.join(folder_path, file))
        player_csvs.append(df)

# Fusionner les DataFrames des joueurs
merged_player_df = pd.concat(player_csvs, axis=0, ignore_index=True)

# Afficher la première colonne du DataFrame fusionné
st.write(merged_player_df.head())

# Streamlit app
st.title("LaLiga Dashboard 2023/24")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Team Statistics", "Player Statistics"])

# Page: Overview
if page == "Overview":
    st.header("Overview of LaLiga 2023/24")
    st.write("Comparison of Home and Away Performance")

    home_table_df = pd.read_csv('Laliga_table_home_2023_24.csv')
    away_table_df = pd.read_csv('Laliga_table_away_2023_24.csv')
    
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
    team_goals_df = dataframes['player_goals_per_90.csv']
    fig_goals = px.bar(team_goals_df, x='Team', y='Goals per Match', title='Goals per Match by Team')
    st.plotly_chart(fig_goals)

    # Team ratings
    st.subheader("Team Ratings")
    team_ratings_df = dataframes['player_player_ratings.csv']
    fig_ratings = px.bar(team_ratings_df, x='Team', y='FotMob Team Rating', title='Team Ratings')
    st.plotly_chart(fig_ratings)

    # Tackles won
    st.subheader("Tackles Won")
    team_tackles_df = dataframes['player_tackles_won.csv']
    fig_tackles = px.bar(team_tackles_df, x='Team', y='Successful Tackles per Match', title='Tackles Won by Team')
    st.plotly_chart(fig_tackles)

# Page: Player Statistics
elif page == "Player Statistics":
    st.header("Player Statistics")
    st.write("Compare performance of players in LaLiga.")

    # Sélection des DataFrames à comparer
    selected_datasets = st.multiselect(
        "Sélectionnez les DataFrames à utiliser:",
        options=list(dataframes.keys()),
        default=list(dataframes.keys())[:2]
    )

    # Sélection des joueurs à comparer
    selected_players = st.multiselect(
        "Sélectionnez les joueurs à comparer:",
        options=dataframes['player_goals_per_90.csv']['Player'].unique(),
        default=dataframes['player_goals_per_90.csv']['Player'].unique()[:2]
    )

    # Filtrage des données des joueurs sélectionnés
    filtered_dfs = {}
    for dataset in selected_datasets:
        filtered_dfs[dataset] = dataframes[dataset][dataframes[dataset]['Player'].isin(selected_players)]

    # Exemple de comparaison avec un radar chart pour un DataFrame
    if 'player_goals_per_90.csv' in selected_datasets:
        df_goals = filtered_dfs['player_goals_per_90.csv']
        fig = go.Figure()

        for player in selected_players:
            player_data = df_goals[df_goals['Player'] == player].iloc[0]
            fig.add_trace(go.Scatterpolar(
                r=[player_data['Goals per Match'], player_data['Total Goals Scored'], player_data['Matches']],
                theta=['Goals per Match', 'Total Goals Scored', 'Matches'],
                fill='toself',
                name=player
            ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, max(df_goals['Goals per Match'].max(), df_goals['Total Goals Scored'].max(), df_goals['Matches'].max())])
            ),
            showlegend=True,
            title='Comparaison des Joueurs'
        )
        st.plotly_chart(fig)
