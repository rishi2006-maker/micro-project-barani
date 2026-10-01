from bs4 import BeautifulSoup
from urllib.parse import urlparse

def analyze_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    forms = soup.find_all("form")
    inputs = soup.find_all("input")
    password_inputs = soup.find_all("input", attrs={"type": lambda x: x and x.lower() == "password"})
    iframes = soup.find_all("iframe")
    scripts = soup.find_all("script")
    links = soup.find_all("a", href=True)
    hidden = soup.find_all(attrs={"style": lambda x: x and "display:none" in x.replace(" ", "").lower()})

    external_links = 0
    for a in links:
        href = a.get("href", "")
        if href.startswith(("http://", "https://")):
            external_links += 1

    features = {
        "html_size": len(html),
        "node_count": len(soup.find_all()),
        "forms": len(forms),
        "inputs": len(inputs),
        "password_inputs": len(password_inputs),
        "iframes": len(iframes),
        "scripts": len(scripts),
        "links": len(links),
        "external_links": external_links,
        "hidden_elements": len(hidden),
        "has_title": bool(soup.title),
        "has_favicon": bool(soup.find("link", rel=lambda x: x and "icon" in str(x).lower())),
    }

    score = 0.0
    if features["password_inputs"]: score += 0.22
    if features["forms"] >= 2: score += 0.10
    if features["iframes"] >= 2: score += 0.10
    if features["hidden_elements"] >= 2: score += 0.10
    if features["external_links"] > 15: score += 0.08
    if features["scripts"] > 20: score += 0.08
    if features["node_count"] > 500: score += 0.06

    return {
        "risk_score": round(min(score, 0.99), 4),
        "risk_level": level(score),
        "features": features,
        "summary": "HTML DOM evidence extracted using prototype HTMLDet-style graph statistics."
    }

def level(score):
    if score >= 0.65:
        return "High"
    if score >= 0.35:
        return "Medium"
    return "Low"
