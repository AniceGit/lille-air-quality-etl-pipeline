import etl.extract as ext
import etl.transform as tr
from datetime import date as dt_date


date = dt_date.today().strftime("%Y-%m-%d")

# date = "2019-05-08"  # Date de l'épisode de pollution
polluant = "04"  # Code du polluant (03 pour Ozone, 05 pour NO2, etc.)

# Fonction principale pour générer et télécharger le fichier
def main():
    # print("Demande de génération du fichier...")
    # file_id = ext.generate_file(date, polluant)
    
    # if file_id:
    #     print("Le fichier a été généré avec succès. Téléchargement en cours...")
    #     ext.download_file(file_id)
    # else:
    #     print("Échec de la génération du fichier. Impossible de continuer.")


    # tr.filter_lille_data()


    ext.download_all_pollutants(date)