# Enhanced PhishDet — Prototype

**Phishing Website Detection Using URL and HTML with Deep Learning**

This repository is a **demonstration prototype** based on the architecture described in the micro project report. The report defines PhishDet as two evidence paths—URLDet (CNN + LSTM) and HTMLDet (graph-based processing)—followed by feature fusion and classification.

## Important scope note

The supplied report states that the GAN enhancement is proposed, local experimental metrics are not verified, and the planned interface was not connected to a verified trained model. This repository therefore does **not** fabricate deep-learning accuracy or GAN results.

The current prototype provides:
- Flask web interface
- URL preprocessing and risk analysis
- Live HTML fetching when the target allows it
- HTML/DOM structural analysis
- URL + HTML evidence fusion
- prediction + confidence display
- synthetic phishing-like URL generator for development only
- clean structure for later insertion of trained CNN/LSTM/GCN models

The prototype's heuristic scores are **not research results** and must not be reported as PhishDet training metrics.

## Architecture

Browser → Flask API → URL evidence + HTML evidence → Fusion → Prediction

Future model replacement:

URL → URLDet (CNN + LSTM)
HTML → DOM graph → HTMLDet (GCN)
Both representations → Fusion → Classifier

## Run locally

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
py app.py
```

Open:

`http://127.0.0.1:5000`

### If PowerShell blocks activation

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## Test

```powershell
python -m pytest
```

## GitHub

```powershell
git init
git add .
git commit -m "Initial Enhanced PhishDet prototype"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/enhanced-phishdet.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Repository structure

```text
enhanced-phishdet/
├── app.py
├── requirements.txt
├── README.md
├── modules/
│   ├── fetcher.py
│   ├── url_detector.py
│   ├── html_detector.py
│   └── fusion.py
├── gan/
│   └── generate_samples.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_prototype.py
```

## Safety

Do not enter passwords, API keys, private URLs, or confidential pages. The prototype may fetch a submitted URL from the machine running Flask. Use only URLs you are authorized to inspect.

## Next step for the actual research implementation

Replace the prototype modules with the verified trained components:
1. URL tokenization → CNN + LSTM URLDet.
2. HTML DOM → graph X/A → GCN/graph pooling HTMLDet.
3. Concatenate learned representations.
4. Train/evaluate on a documented labelled dataset.
5. Add the GAN enhancement only after implementing and testing it.
6. Store trained models under `models/` and connect the Flask endpoint.
7. Report only measured metrics from the actual test set.
