import pandas as pd
import os

def filter_lille_data(filepath="data/air_quality_data.csv", output_path="data/air_quality_lille.csv"):
    """
    Filtre les données de qualité de l'air pour ne garder que celles concernant la ville de Lille.

    :param filepath: Chemin du fichier CSV brut téléchargé.
    :param output_path: Chemin du fichier CSV filtré à sauvegarder.
    """
    if not os.path.exists(filepath):
        print(f"❌ Fichier introuvable : {filepath}")
        return

    try:
        df = pd.read_csv(filepath, sep=';')

        if 'Zas' not in df.columns:
            print("❌ La colonne 'Zas' est absente du fichier.")
            return

        df_lille = df[df['Zas'].str.contains("ZAG LILLE", case=False, na=False)]

        if df_lille.empty:
            print("⚠️ Aucun enregistrement trouvé pour Lille.")
        else:
            df_lille.to_csv(output_path, index=False)
            print(f"✅ {len(df_lille)} lignes concernant Lille ont été sauvegardées dans : {output_path}")

    except Exception as e:
        print(f"❌ Erreur lors du traitement du fichier : {e}")
