from modules.url_detector import analyze_url
from modules.html_detector import analyze_html
from modules.fusion import fuse_scores

def test_url_analysis():
    result = analyze_url("https://example.com")
    assert 0 <= result["risk_score"] <= 1
    assert "features" in result

def test_html_analysis():
    html = "<html><body><form><input type='password'></form></body></html>"
    result = analyze_html(html)
    assert result["features"]["password_inputs"] == 1
    assert 0 <= result["risk_score"] <= 1

def test_fusion():
    result = fuse_scores(0.8, 0.7)
    assert result["prediction"] == "Phishing Website"
    assert 0 <= result["confidence"] <= 100
