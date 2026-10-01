const $ = (id) => document.getElementById(id);

function showFeatures(target, features) {
  target.innerHTML = "";
  Object.entries(features || {}).forEach(([key, value]) => {
    const div = document.createElement("div");
    div.className = "feature";
    div.innerHTML = `<b>${key.replaceAll("_", " ")}</b><br>${String(value)}`;
    target.appendChild(div);
  });
}

async function analyze() {
  const url = $("url").value.trim();
  $("error").classList.add("hidden");
  $("result").classList.add("hidden");
  if (!url) {
    $("error").textContent = "Enter a website URL first.";
    $("error").classList.remove("hidden");
    return;
  }

  $("loading").classList.remove("hidden");
  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({url})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Analysis failed.");

    $("prediction").textContent = data.fusion.prediction;
    $("confidence").textContent = `Confidence: ${data.fusion.confidence}%`;
    $("score").textContent = `${(data.fusion.risk_score * 100).toFixed(1)}%`;

    $("urlLevel").textContent = `Risk: ${data.url_analysis.risk_level}`;
    $("urlSummary").textContent = data.url_analysis.summary;
    showFeatures($("urlFeatures"), data.url_analysis.features);

    $("htmlLevel").textContent = `Risk: ${data.html_analysis.risk_level}`;
    $("htmlSummary").textContent = data.html_analysis.summary;
    showFeatures($("htmlFeatures"), data.html_analysis.features);

    $("notice").textContent = data.prototype_notice;
    if (data.fetch_error) {
      $("htmlSummary").textContent += " Live HTML fetch failed, so HTML evidence was not included in fusion.";
    }
    $("result").classList.remove("hidden");
  } catch (e) {
    $("error").textContent = e.message;
    $("error").classList.remove("hidden");
  } finally {
    $("loading").classList.add("hidden");
  }
}

$("analyze").addEventListener("click", analyze);
$("url").addEventListener("keydown", (e) => { if (e.key === "Enter") analyze(); });
document.querySelectorAll(".example").forEach(btn => {
  btn.addEventListener("click", () => {
    $("url").value = btn.dataset.url;
    analyze();
  });
});
