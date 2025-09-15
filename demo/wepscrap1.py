import requests
from bs4 import BeautifulSoup

# URL d'exemple (site statique, idéal pour tester BeautifulSoup)
url = "https://realpython.github.io/fake-jobs/"

# Télécharger la page HTML
response = requests.get(url)
html = response.text

# Créer l'objet BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Trouver tous les titres des jobs (balises <h2> avec la classe "title")
job_titles = soup.find_all("h2", class_="title")

# Afficher les 5 premiers titres
for i, job in enumerate(job_titles[:5], start=1):
    print(f"{i}. {job.text.strip()}")
