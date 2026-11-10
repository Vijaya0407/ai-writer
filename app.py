import os
import re
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

def seo_score(title, meta, keywords, content):
    """A simple transparent on-page SEO checklist score (0-100)."""
    score = 0
    checks = []
    title_len = len(title.strip())
    meta_len = len(meta.strip())
    words = re.findall(r"\b[\w'-]+\b", content.lower())
    word_count = len(words)
    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    first_paragraph = content[:500].lower()

    def add(condition, points, good, improve):
        nonlocal score
        if condition:
            score += points
            checks.append({"ok": True, "text": good, "points": points})
        else:
            checks.append({"ok": False, "text": improve, "points": points})

    add(30 <= title_len <= 60, 20, "SEO title is within 30–60 characters.",
        "Keep the SEO title between 30 and 60 characters.")
    add(120 <= meta_len <= 160, 20, "Meta description is within 120–160 characters.",
        "Write a meta description of 120–160 characters.")
    add(bool(keyword_list), 10, "At least one target keyword is provided.",
        "Add one or more target keywords.")
    add(any(k in content.lower() for k in keyword_list), 15,
        "A target keyword appears in the content.",
        "Include a target keyword naturally in the content.")
    add(any(k in first_paragraph for k in keyword_list), 10,
        "A target keyword appears near the beginning.",
        "Include a target keyword naturally in the opening paragraph.")
    add(word_count >= 300, 10, f"Content has {word_count} words (300+).",
        f"Expand the content to at least 300 words (currently {word_count}).")
    add(bool(re.search(r"^##?\s+", content, re.M)), 5,
        "Content uses headings.", "Add clear headings to structure the article.")
    add(bool(re.search(r"(?m)^\s*[-*]\s+", content)), 5,
        "Content includes a scannable list.", "Add a short bullet list where useful.")
    add(bool(re.search(r"\b(conclusion|in summary|final thoughts)\b", content, re.I)), 5,
        "Content has a conclusion or summary.", "Add a brief conclusion or summary.")
    return {"score": score, "checks": checks, "word_count": word_count}

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/generate")
def generate():
    data = request.get_json(silent=True) or {}
    topic = (data.get("topic") or "").strip()
    keywords = (data.get("keywords") or "").strip()
    content_type = (data.get("content_type") or "Blog post").strip()
    tone = (data.get("tone") or "Professional").strip()
    audience = (data.get("audience") or "General readers").strip()
    language = (data.get("language") or "English").strip()
    length = (data.get("length") or "Medium (600–900 words)").strip()

    if len(topic) < 4:
        return jsonify({"error": "Please enter a topic with at least 4 characters."}), 400
    if len(topic) > 300:
        return jsonify({"error": "Topic must be 300 characters or fewer."}), 400

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({
            "error": "AI generation is not configured yet. Add your OPENAI_API_KEY to a .env file. The SEO checker works after generation."
        }), 503

    try:
        client = OpenAI(api_key=api_key)
        prompt = f"""
You are an expert SEO content writer. Create original, useful, reader-first content.
Topic: {topic}
Content format: {content_type}
Target keywords: {keywords or "Choose relevant natural keywords"}
Audience: {audience}
Tone: {tone}
Language: {language}
Desired length: {length}

Return exactly these sections using Markdown:
# SEO Title
(one compelling title, ideally 30–60 characters)
# Meta Description
(one accurate description, ideally 120–160 characters)
# Suggested URL Slug
(short, lowercase, hyphen-separated)
# Article
(write the complete content with useful H2/H3 headings, natural keyword use,
a clear introduction, practical details, and a conclusion; avoid keyword stuffing)
# Related Keywords
(5–8 relevant phrases)
# FAQ
(3 concise questions and answers)

Do not invent statistics, citations, testimonials, or factual claims. If a claim needs
verification, flag it briefly instead of making it up.
"""
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You create accurate, helpful, search-friendly content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        result = response.choices[0].message.content or ""
        title_match = re.search(r"(?im)^# SEO Title\s*\n(.+)", result)
        meta_match = re.search(r"(?im)^# Meta Description\s*\n(.+)", result)
        title = title_match.group(1).strip() if title_match else ""
        meta = meta_match.group(1).strip() if meta_match else ""
        score = seo_score(title, meta, keywords, result)
        return jsonify({"content": result, "seo": score, "title": title, "meta": meta})
    except Exception as exc:
        app.logger.exception("Content generation failed")
        return jsonify({"error": "Content generation failed. Check your API key, model name, and internet connection. Details: " + str(exc)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
