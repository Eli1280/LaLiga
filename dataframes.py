import pandas as pd
import glob
# Liste des fichiers CSV
files = [
    'team_goals_per_match.csv',
    'team_ratings.csv',
    'total_red_card_team.csv',
    'total_yel_card_team.csv',
    'touches_in_opp_box_team.csv',
    'won_tackle_team.csv',
    'player_goals_per_90.csv',
    'player_interceptions.csv',
    'player_on_target_scoring_attempts.csv',
    'player_outfielder_blocks.csv',
    'player_penalties_conceded.csv',
    'player_penalties_won.csv',
    'player_player_ratings.csv',
    'player_possessions_won_attacking_third.csv',
    'player_red_cards.csv',
    'player_saves_made.csv',
    'player_tackles_won.csv',
    'player_top_assists.csv',
    'player_top_scorers.csv',
    'player_total_assists_in_attack.csv',
    'player_total_scoring_attempts.csv',
    'player_yellow_cards.csv',
    'possession_percentage_team.csv',
    'possession_won_att_3rd_team.csv',
    'saves_team.csv',
    'goals_conceded_team_match.csv',
    'interception_team.csv',
    'ontarget_scoring_att_team.csv',
    'penalty_conceded_team.csv',
    'penalty_won_team.csv',
    'player_accurate_long_balls.csv',
    'player_accurate_passes.csv',
    'player_big_chances_created.csv',
    'player_big_chances_missed.csv',
    'player_clean_sheets.csv',
    'player_contests_won.csv',
    'player_effective_clearances.csv',
    'player_expected_assists.csv',
    'player_expected_assists_per_90.csv',
    'player_expected_goals.csv',
    'player_expected_goals_on_target.csv',
    'player_expected_goals_per_90.csv',
    'player_fouls_committed.csv',
    'player_goals_conceded.csv',
    'accurate_cross_team.csv',
    'accurate_long_balls_team.csv',
    'accurate_pass_team.csv',
    'big_chance_missed_team.csv',
    'big_chance_team.csv',
    'clean_sheet_team.csv',
    'corner_taken_team.csv',
    'effective_clearance_team.csv',
    'expected_goals_conceded_team.csv',
    'expected_goals_team.csv',
    'fk_foul_lost_team.csv'
]

# Fonction pour charger les fichiers CSV dans un dictionnaire
def load_dataframes(file_list):
    dataframes = {}
    for file in file_list:
        df_name = file.split('.')[0]  # Utiliser le nom du fichier sans l'extension
        dataframes[df_name] = pd.read_csv(f'data/{file}')
    return dataframes

