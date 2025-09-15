import requests
from bs4 import BeautifulSoup

url = "https://realpython.github.io/fake-jobs/"



resp = requests.get(url)
html = resp.text
soup = BeautifulSoup(html, "html.parser")

job_titles = soup.select("h2.title")
# job_titles = soup.find_all("h2", class_="title")

for jt in job_titles:
    print(jt.get_text(strip=True))
