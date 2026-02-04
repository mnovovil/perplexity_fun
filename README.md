# Perplexity API Local Query System Chatbot

This project provides a set up to interact with Perplexity from a local terminal, no need to go into web.

## Setup

### 1. Prerequisites

- Docker
- Docker Compose (optional)
- Perplexity API key (get it from [Perplexity](https://www.perplexity.ai/))

### 2. Installation

1. Clone or navigate to this directory
2. Copy the environment template and add your API key:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your Perplexity API key:
   ```
   PERPLEXITY_API_KEY=your_actual_api_key_here
   ```

### 3. Running Locally (without Docker)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your API key:
   ```bash
   export PERPLEXITY_API_KEY=your_actual_api_key_here
   ```

3. Run a query:
   ```bash
   python src/query.py
   ```

### 4. Local terminal deployment (no browser)

You can build and run the Perplexity client entirely from the terminal — no browser required. The repo includes two helper scripts in `scripts/` to simplify this on Windows.

Quick Setup (one command)

Run this single command to create a Desktop shortcut that builds the image and lets you enter queries interactively:

```powershell
powershell -ExecutionPolicy Bypass -File "C:\miguel\perplexity\scripts\create_shortcut.ps1" -AttemptPinToTaskbar
```

How to use the shortcut

- Double-click the `Build Perplexity` shortcut on your Desktop.
- The shortcut builds the Docker image, then prompts: `Enter prompt to send to Perplexity (leave empty to finish)`.
- Type your query (for example: `Tell me about Salinas, Asturias`) and press Enter; the response prints to the window.
- Press Enter on an empty line to finish and close the window.

- `scripts/build_perplexity.ps1` — builds the Docker image and then prompts you for queries; each query is sent to the container and the response printed.
- `scripts/create_shortcut.ps1` — creates a Desktop shortcut that runs the build script (optional).

Quick manual commands

1. Build the Docker image:
   ```powershell
   docker build -t perplexity-api .
   ```

2a. Run a single prompt (pass prompt as an argument):
   ```powershell
   docker run --rm --env-file .env perplexity-api "Tell me about Salinas, Asturias"
   ```

2b. Or run by invoking the Python inside the image (more reliable if you hit TTY/stdin issues):
   ```powershell
   docker run --rm --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python perplexity-api /app/src/query.py "Tell me about Salinas, Asturias"
   ```

2c. Pipe a prompt into the container (good for multi-line input):
   ```powershell
   echo "Tell me about Salinas, Asturias" | docker run --rm -i --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python perplexity-api /app/src/query.py
   ```

Using the included Windows helper (recommended once you're comfortable)

1. Create a desktop shortcut (one-time):
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts\create_shortcut.ps1 -AttemptPinToTaskbar
   ```

2. Run the shortcut (double-click) — it will build the image and then prompt you to enter queries interactively. Type your query (for example: "Tell me about Salinas, Asturias") and press Enter. Repeat until you press Enter on an empty line.

Notes and troubleshooting

- Always store your key in `.env` (use `.env.example` as a template) and pass it with `--env-file .env` when running the container.
- If `docker run ... "No prompt provided"` appears, use the `--entrypoint` override shown above or use the `scripts/build_perplexity.ps1` helper which handles argument forwarding.
- To inspect the Python path inside the image if the path differs on your system:
  ```powershell
  docker run --rm perplexity-api ls /opt/conda/envs
  docker run --rm perplexity-api which python || docker run --rm perplexity-api ls /opt/conda/envs/appenv/bin/python
  ```
- Use `--rm` to remove the container after it runs.

## Project Structure
```
perplexity/
├── .env                 # Local environment file (not committed)
├── .perplexity/         # Local session storage (session.json)
├── Dockerfile           # Docker configuration
├── entrypoint.sh        # Container entrypoint script
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── scripts/             # Helper scripts (Windows)
│   ├── build_perplexity.ps1
│   └── create_shortcut.ps1
└── src/                 # Source code
   ├── cli.py           # CLI helpers (store/show key)
   ├── config.py        # Configuration and keyring helpers
   ├── queries.py       # Predefined queries
   ├── query.py         # Main script for querying the API
   └── session.py       # QueryClient with persistent chat memory
```

## Usage

### Basic Query

```python
from src.query import query_perplexity

response = query_perplexity("What are the latest developments in AI?")
print(response)
```

### Using Predefined Queries

```python
from src.query import query_perplexity
from src.queries import get_query

# Get a predefined query
question = get_query("ai_developments")
response = query_perplexity(question)
print(response)
```

### Available Presets

- `pro-search`: Best for research-heavy queries
- `pro`: Standard professional preset
- `stable-diffusion`: For image-related queries
- `fast`: Fastest response time

## Environment Variables

- `PERPLEXITY_API_KEY`: Your Perplexity API key (required)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR) (optional, default: INFO)

## Files

- **query.py**: Main script containing the `query_perplexity()` function
- **queries.py**: Module with predefined queries and available pres ets
- **config.py**: Configuration management and validation
- **Dockerfile**: Docker image configuration
- **.env.example**: Template for environment variables

## Notes

- Never commit your `.env` file with actual API keys to version control
- The `.env.example` file is safe to commit as it contains no sensitive data
- Ensure your API key has the necessary permissions for the desired operations

## Troubleshooting

### "PERPLEXITY_API_KEY environment variable is not set"
Make sure you have created a `.env` file with your API key and that it's in the correct format.

### "ModuleNotFoundError: No module named 'perplexity'"
Install the dependencies:
```bash
pip install -r requirements.txt
```

### Docker build issues
Ensure Docker is running and you have sufficient disk space:
```bash
docker system prune  # Free up space
docker build -t perplexity-api .
```

## Session Memory, Secure Key Storage, and Docker Mounting

This project now supports a persistent chat memory and optional secure API key storage:

- Session memory: the client saves a small conversation history (`session.json`) so the chat can "remember" past user messages and assistant replies. The session file is stored by default in the user's data folder (`~/.perplexity/session.json`) inside the container.
- Secure key storage: you can store your `PERPLEXITY_API_KEY` in the OS keyring using the included CLI helper. The code will prefer `PERPLEXITY_API_KEY` from the environment, then fall back to the OS keyring.

Usage examples:

- Store the API key in the system keyring (recommended):
```powershell
python src/cli.py store-key --key YOUR_API_KEY
```

- Check whether a key is configured:
```powershell
python src/cli.py show-key
```

- Run queries while preserving memory between runs (Windows helper builds and mounts automatically):
   - Use the `scripts/build_perplexity.ps1` helper that will create a local `.perplexity` folder and mount it into the container so `session.json` is reused between container runs.
   - Alternatively, mount a host directory yourself when running the container:
```powershell
docker run --rm -it -v C:\path\to\repo\.perplexity:/root/.perplexity --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python perplexity-api /app/src/query.py "Where is Williamsburg, NYC?"
```

Notes on Docker on Windows:
- If Docker path mounting fails due to Windows path formatting, use the `scripts/build_perplexity.ps1` helper which handles mounting for you, or use a named Docker volume instead:
```powershell
docker volume create perplexity_session
docker run --rm -it -v perplexity_session:/root/.perplexity --env-file .env --entrypoint /opt/conda/envs/appenv/bin/python perplexity-api /app/src/query.py "Hello"
```

Security and best practices:
- Do not commit your `.env` with real secrets. Prefer storing the key in the keyring or pass it via environment variables at runtime.
- If you need to rotate keys, update the keyring entry or the `.env` file and restart the container.

