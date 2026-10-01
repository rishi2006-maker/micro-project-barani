from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
from modules.url_detector import analyze_url
from modules.html_detector import analyze_html
from modules.fusion import fuse_scores
from modules.fetcher import fetch_page

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "Please enter a URL."}), 400

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    url_result = analyze_url(url)

    # Prototype can analyze a live page when reachable. If fetching fails,
    # URL-only evidence is still returned rather than pretending HTML was analyzed.
    html_result = None
    fetch_error = None
    try:
        html = fetch_page(url)
        html_result = analyze_html(html)
    except Exception as exc:
        fetch_error = str(exc)
        html_result = {
            "risk_score": 0.0,
            "risk_level": "Unavailable",
            "features": {},
            "summary": "HTML could not be fetched; result uses URL evidence only."
        }

    result = fuse_scores(url_result["risk_score"], html_result["risk_score"], html_available=not bool(fetch_error))

    return jsonify({
        "url": url,
        "url_analysis": url_result,
        "html_analysis": html_result,
        "fusion": result,
        "fetch_error": fetch_error,
        "prototype_notice": "Prototype heuristic inference. Not a verified trained PhishDet model."
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
