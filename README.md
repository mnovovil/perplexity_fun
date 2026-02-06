# Perplexity — Promp perplexity directly from terminal

Quick PowerShell steps to install and run (Windows):

1. Store your API key in the OS wkeyring (preferred):

```powershell
python src/cli.py store-key --key YOUR_API_KEY
```

2. Run the setup script to install globally (one-time setup):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_perplexity_global.ps1
```

3. Once installed, simply run `px` from any terminal to start Perplexity:

```powershell
px "insert your prompt"
```

If you prefer a one-shot Docker command instead of the helper:

```powershell
docker build -t perplexity-api .
docker run --rm --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python perplexity-api /app/src/query.py "Where is Williamsburg, NYC?"
```

That's all — the session file is stored at `.perplexity/session.json` in the repo when you use the helper.

