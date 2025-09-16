import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

URLS = [
    "https://fr.wikipedia.org/wiki/Graham_Chapman",
    "https://fr.wikipedia.org/wiki/John_Cleese",
    "https://fr.wikipedia.org/wiki/Terry_Gilliam",
    "https://fr.wikipedia.org/wiki/Eric_Idle",
    "https://fr.wikipedia.org/wiki/Terry_Jones",
    "https://fr.wikipedia.org/wiki/Michael_Palin"
]

UA = "EduScraper/1.0 (+https://exemple.com/contact)"

def fetch(url):
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=10)
    return url, resp.status_code, len(resp.text)

def main():
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(fetch, url) for url in URLS]
        for f in as_completed(futures):
            url, status, size = f.result()
            print(f"{url} → {status}, {size} caractères")

if __name__ == "__main__":
    main()
