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

## Testing

Run tests locally with pytest:

```powershell
# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run tests with coverage report
pytest tests/ -v --cov=src --cov-report=html
```

Tests are automatically run on every push and pull request via GitHub Actions. See [.github/workflows/pytest.yml](.github/workflows/pytest.yml) for the workflow configuration.

