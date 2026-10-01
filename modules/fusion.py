def fuse_scores(url_score, html_score, html_available=True):
    # Prototype approximation of the report's URL + HTML feature fusion.
    if html_available:
        combined = 0.55 * url_score + 0.45 * html_score
    else:
        combined = url_score

    combined = round(max(0.0, min(combined, 0.99)), 4)
    label = "Phishing Website" if combined >= 0.50 else "Likely Legitimate"
    confidence = round((combined if label.startswith("Phishing") else 1 - combined) * 100, 2)

    return {
        "risk_score": combined,
        "prediction": label,
        "confidence": confidence,
        "method": "Weighted URL + HTML prototype fusion"
    }
