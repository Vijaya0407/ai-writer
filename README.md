# WriteWise AI — AI-Powered Content Creation & SEO Writing

WriteWise AI is a beginner-friendly portfolio project that generates SEO-oriented content from a writing brief and evaluates the draft with a transparent on-page SEO checklist.

## Features

- Generate blog posts, product descriptions, landing-page copy, social posts, and email newsletters.
- Choose tone, audience, language (English, Telugu, or bilingual), and length.
- Provide target SEO keywords.
- Generate an SEO title, meta description, URL slug, article, related keywords, and FAQs.
- Basic SEO readiness score with actionable checks.
- Copy the draft or download it as a Markdown file.
- Responsive interface for desktop and mobile.
- API key is read on the Python server, not exposed in browser JavaScript.

## Tech stack

- Python 3
- Flask
- OpenAI API
- HTML, CSS, JavaScript

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and add your API key:

   ```env
   OPENAI_API_KEY=your_real_api_key
   OPENAI_MODEL=gpt-4o-mini
   ```

6. Start the app:

   ```bash
   python app.py
   ```

7. Open `http://127.0.0.1:5000` in your browser.

## Important security notes

- Never upload `.env` or your API key to GitHub.
- `.gitignore` already excludes `.env`; keep it that way.
- If an API key is accidentally published, revoke it and create a new one.
- AI-generated text can contain errors. Verify facts, sources, originality, and claims before publishing.

## SEO score explanation

The score is a simple educational checklist based on title length, meta description length, keyword usage, word count, headings, a list, and a conclusion. It is **not** a Google ranking predictor and does not guarantee search performance.

## Suggested GitHub repository description

`An AI-powered content creation and SEO writing web app built with Flask, Python, HTML, CSS, JavaScript, and the OpenAI API.`

## Future improvements

- Save and manage previous drafts in a database.
- Add readability and plagiarism-check integrations.
- Add keyword research using a trusted SEO data provider.
- Add user authentication and export to PDF/DOCX.
- Add automated tests and deployment configuration.
