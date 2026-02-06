# Perplexity from terminal

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

That's all — the session file is stored at `.perplexity/session.json` in the repo when you use the helper.

