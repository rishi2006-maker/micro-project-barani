import requests

def fetch_page(url: str) -> str:
    headers = {
        "User-Agent": "Enhanced-PhishDet-Prototype/1.0"
    }
    response = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
    response.raise_for_status()
    if "text/html" not in response.headers.get("Content-Type", ""):
        raise ValueError("The URL did not return an HTML page.")
    return response.text[:2_000_000]
