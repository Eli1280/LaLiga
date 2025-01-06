import pandas as pd
import glob

# Charger automatiquement tous les fichiers CSV dans le dossier 'data'
def load_dataframes(path='data/*.csv'):
    files = glob.glob(path)
    dataframes = {}
    for file in files:
        df_name = file.split('/')[-1].replace('.csv', '')  # Utilise le nom du fichier comme clé
        dataframes[df_name] = pd.read_csv(file)
    return dataframes
