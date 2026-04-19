import httpx

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

def search_pubmed(query: str):
    params = {
        "db": "pubmed",
        "retmode": "json",
        "term": query,
        "retmax": 5,
    }
    r = httpx.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    q = "treatment A treatment B survival"
    data = search_pubmed(q)
    print(data)
