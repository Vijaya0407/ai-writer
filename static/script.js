const form = document.getElementById("writer-form");
const generateBtn = document.getElementById("generate-btn");
const emptyState = document.getElementById("empty-state");
const loading = document.getElementById("loading");
const errorBox = document.getElementById("error");
const result = document.getElementById("result");
const output = document.getElementById("content-output");
let latestContent = "";

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  emptyState.classList.add("hidden");
  result.classList.add("hidden");
  errorBox.classList.add("hidden");
  loading.classList.remove("hidden");
  generateBtn.disabled = true;
  generateBtn.innerHTML = "<span>✦</span> Generating… <span>…</span>";

  const payload = {
    topic: document.getElementById("topic").value,
    content_type: document.getElementById("content_type").value,
    tone: document.getElementById("tone").value,
    language: document.getElementById("language").value,
    length: document.getElementById("length").value,
    keywords: document.getElementById("keywords").value,
    audience: document.getElementById("audience").value
  };

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    latestContent = data.content;
    output.textContent = data.content;
    showSEO(data.seo);
    result.classList.remove("hidden");
  } catch (error) {
    errorBox.textContent = error.message;
    errorBox.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
    generateBtn.disabled = false;
    generateBtn.innerHTML = "<span>✦</span> Generate content <span>→</span>";
  }
});

function showSEO(seo) {
  document.getElementById("score-number").textContent = seo.score;
  document.getElementById("progress-fill").style.width = `${seo.score}%`;
  document.getElementById("word-count").textContent = `Approximate word count: ${seo.word_count}`;
  const list = document.getElementById("seo-checks");
  list.replaceChildren();
  seo.checks.forEach(check => {
    const item = document.createElement("li");
    item.className = check.ok ? "ok" : "bad";
    item.textContent = `${check.ok ? "✓" : "○"}  ${check.text}`;
    list.appendChild(item);
  });
}

document.getElementById("copy-btn").addEventListener("click", async () => {
  if (!latestContent) return;
  await navigator.clipboard.writeText(latestContent);
  document.getElementById("copy-btn").textContent = "Copied!";
  setTimeout(() => document.getElementById("copy-btn").textContent = "Copy", 1500);
});

document.getElementById("download-btn").addEventListener("click", () => {
  if (!latestContent) return;
  const blob = new Blob([latestContent], {type: "text/markdown;charset=utf-8"});
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "writewise-ai-content.md";
  link.click();
  URL.revokeObjectURL(url);
});
