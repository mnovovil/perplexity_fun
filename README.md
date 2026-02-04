# Perplexity — Quick PowerShell Install to Run Chatbot Locally

Quick PowerShell steps to install and run (Windows):

1. Store your API key in the OS wkeyring (preferred):

```powershell
python src/cli.py store-key --key YOUR_API_KEY
```

2. Build and run using the included helper (creates and mounts `.perplexity` so session is preserved):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_perplexity.ps1
```

3. When prompted, type your question and press Enter. Press Enter on an empty line to finish.

If you prefer a one-shot Docker command instead of the helper:

```powershell
docker build -t perplexity-api .
docker run --rm --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python perplexity-api /app/src/query.py "Where is Williamsburg, NYC?"
```

That's all — the session file is stored at `.perplexity/session.json` in the repo when you use the helper.

