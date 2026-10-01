from urllib.parse import urlparse
import ipaddress
import math
import re

SUSPICIOUS_WORDS = {
    "login", "signin", "verify", "verification", "secure", "account",
    "update", "confirm", "password", "wallet", "bank", "bonus",
    "free", "gift", "claim", "recover", "unlock"
}

def _entropy(text):
    if not text:
        return 0.0
    counts = {c: text.count(c) for c in set(text)}
    n = len(text)
    return -sum((v/n) * math.log2(v/n) for v in counts.values())

def analyze_url(url: str):
    p = urlparse(url)
    host = p.netloc.lower()
    path = p.path.lower()
    full = url.lower()

    features = {
        "url_length": len(url),
        "host_length": len(host),
        "dot_count": host.count("."),
        "hyphen_count": host.count("-"),
        "at_symbol": "@" in url,
        "ip_address": False,
        "https": p.scheme == "https",
        "suspicious_words": sorted(w for w in SUSPICIOUS_WORDS if w in full),
        "query_parameter_count": len([x for x in p.query.split("&") if x]),
        "subdomain_depth": max(0, len(host.split(".")) - 2),
        "entropy": round(_entropy(host), 3),
    }

    try:
        ipaddress.ip_address(p.hostname or "")
        features["ip_address"] = True
    except ValueError:
        pass

    score = 0.0
    if features["url_length"] > 75: score += 0.18
    if features["url_length"] > 120: score += 0.10
    if features["host_length"] > 35: score += 0.10
    if features["hyphen_count"] >= 2: score += 0.08
    if features["dot_count"] >= 4: score += 0.08
    if features["subdomain_depth"] >= 2: score += 0.10
    if features["at_symbol"]: score += 0.18
    if features["ip_address"]: score += 0.22
    if features["suspicious_words"]: score += min(0.25, 0.06 * len(features["suspicious_words"]))
    if p.scheme != "https": score += 0.08
    if features["entropy"] > 4.0: score += 0.08

    score = min(score, 0.99)
    return {
        "risk_score": round(score, 4),
        "risk_level": level(score),
        "features": features,
        "summary": "URL evidence extracted using prototype URLDet-style preprocessing."
    }

def level(score):
    if score >= 0.65:
        return "High"
    if score >= 0.35:
        return "Medium"
    return "Low"
