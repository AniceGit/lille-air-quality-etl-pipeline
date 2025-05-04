import requests
import time
import pandas as pd
import etl.transform as tr

# Remplace par ta clé API obtenue après inscription
API_KEY = "BiLaEEJJkh3XrxKk5EFGBXgdqne1TJvc"

POLLUTANTS = [
    "01", "03", "04", "08", "12", "19", "24", "39",
    "80", "82", "87", "P6", "V4"
]

# Étape 1 : Demander la génération du fichier
def generate_file(date, polluant):
    # URL pour demander la génération du fichier
    url_generation = f"https://www.geodair.fr/api-ext/MoyH/export?date={date}&polluant={polluant}"
    
    # Ajouter l'API key dans les headers
    headers = {
        "apikey": API_KEY
    }
    
    # Effectuer la requête
    try:
        response = requests.get(url_generation, headers=headers)
        
        # Vérifier si la réponse est valide
        response.raise_for_status()  # Soulever une exception pour les erreurs HTTP
        
        # Si la réponse est vide, afficher un message d'erreur
        if not response.text:
            print("La réponse du serveur est vide.")
            return None
        
        # Afficher le contenu de la réponse pour débogage
        print("Réponse de l'API : ", response.text)
        
        # L'API retourne un texte brut (ID du fichier) et non du JSON
        file_id = response.text.strip()  # Enlever les espaces blancs autour de l'ID
        
        if not file_id:
            print("Aucun identifiant de fichier trouvé dans la réponse.")
            return None
        
        print(f"Fichier généré avec succès ! ID du fichier : {file_id}")
        return file_id

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP : {e}")
        return None

# Étape 2 : Télécharger le fichier généré
def download_file(file_id):
    # URL pour télécharger le fichier
    url_download = f"https://www.geodair.fr/api-ext/download?id={file_id}"
    
    # Ajouter l'API key dans les headers
    headers = {
        "apikey": API_KEY
    }
    
    # Vérifier que le fichier est prêt et le télécharger
    file_ready = False
    while not file_ready:
        print("Vérification de la disponibilité du fichier...")
        response = requests.get(url_download, headers=headers)
        
        if response.status_code == 200:
            # Sauvegarder le fichier localement
            with open("data/air_quality_data.csv", "wb") as f:
                f.write(response.content)
            print("Fichier téléchargé avec succès !")
            file_ready = True
        else:
            print("Le fichier n'est pas encore prêt. Nouvelle tentative dans 5 secondes...")
            time.sleep(5)  # Attendre 5 secondes avant de réessayer

def download_all_pollutants(date):
    for pol in POLLUTANTS:
        try:
            print(f"🔄 Traitement du polluant {pol}...")
            print(f"Demande de génération du fichier {file_id}...")
            file_id = generate_file(date, pol)
            if file_id:
                print(f"📁 ID du fichier : {file_id}")
                download_file(file_id)
                tr.filter_lille_data("data/air_quality_data.csv",f"data/{pol}_air_quality_lille.csv")
            else:
                print(f"⚠️ Échec pour le polluant {pol}")
        except Exception as e:
            print(f"❌ Erreur pour {pol} : {e}")

        # Pause pour éviter l'erreur 429
        time.sleep(10)  # Attendre 10 secondes entre chaque appel


