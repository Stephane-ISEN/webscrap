import requests  # Bibliothèque pour envoyer des requêtes HTTP
import os
import time  # à ajouter en haut du fichier
from bs4 import BeautifulSoup  # à ajouter en haut du fichier
import json  # à ajouter en haut du fichier
from urllib.parse import urljoin  # à ajouter en haut du fichier

# Étape 1 : définir l'URL de la page à télécharger
URL = "https://www.francetvinfo.fr/"

# Étape 2 : envoyer une requête HTTP GET pour récupérer le contenu de la page
# On ajoute un en-tête "User-Agent" pour que le site nous traite comme un vrai navigateur
resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})

# Étape 3 : vérifier si la requête a réussi
if resp.status_code == 200:
    # Si le serveur a répondu "200 OK", on affiche un message
    print("Succès ! Contenu de la page récupéré.")
    # On affiche les 500 premiers caractères du code HTML pour voir à quoi cela ressemble
    #print(resp.text[:500])

    # S'assurer que le répertoire "scrap" existe, sinon le créer
    os.makedirs("./scrap", exist_ok=True)

    # Nouveau morceau de code pour écrire le HTML dans un fichier local
    with open("./scrap/page_francetvinfo.html", "w", encoding="utf-8") as f:
        f.write(resp.text)

else:
    # Si la réponse n’est pas 200, on affiche le code d’erreur (ex : 404, 500…)
    print(f"Erreur : statut {resp.status_code}")

# Étape 1 : créer un objet BeautifulSoup à partir du HTML téléchargé
soup = BeautifulSoup(resp.text, "html.parser")
articles = {}

# Étape 2 : sélectionner tous les éléments a.card-article-majeure__link de la page
all_a = soup.select("a.card-article-majeure__link")

# Étape 3 : stocker les titres et les liens dans un diconnaire
for a in all_a:
    href = a.get("href")
    full_url = urljoin(URL, href)  # reconstitution de l’URL complète
     
    try: 
        time.sleep(0.5)  # Pause de 0.5 seconde entre les requêtes
        resp_article = requests.get(full_url, headers={"User-Agent": "Mozilla/5.0"})

        article_soup = BeautifulSoup(resp_article.text, "html.parser")
        title = article_soup.select_one("h1.c-title").get_text(strip=True)
        print(title)
        article = article_soup.select_one("div.c-body").get_text(strip=True)
        
        if href and title:
            articles[title] = title, article 
        
    except requests.RequestException as e:
        print(f"[WARN] Impossible de charger {full_url} : {e}")


# Étape 5 : écrire le dictionnaire dans un fichier JSON
with open("./scrap/articles_francetvinfo.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

