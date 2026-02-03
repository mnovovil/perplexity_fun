# Perplexity API Query System

This project provides a Docker-based setup to interact with the Perplexity API for running AI-powered queries.

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

### 4. Running with Docker (terminal-only)

This repository is configured to be used entirely from the terminal using Docker. The image includes a small CLI wrapper so you can pass a prompt as an argument or pipe text into the container.

1. Build the Docker image:
   ```bash
   docker build -t perplexity-api .
   ```

2. Run the container with a prompt as an argument:
   ```bash
   docker run --rm --env-file .env perplexity-api "Tell me about Salinas, Asturias"
   ```

3. Or pipe a prompt into the container (recommended for multi-line prompts):
   ```bash
   echo "Tell me about Salinas, Asturias" | docker run --rm --env-file .env -i perplexity-api
   ```

4. To specify a different preset, set `PERPLEXITY_PRESET` in your `.env` or pass it as an env var:
   ```bash
   docker run --rm --env-file .env -e PERPLEXITY_PRESET=pro perplexity-api "Your question here"
   ```

Notes:
- Always keep your API key in `.env` and pass it with `--env-file .env`.
- The container will print the question and the API response to stdout.
- Use `--rm` to remove the container after it runs.

## Project Structure

```
perplexity/
├── Dockerfile           # Docker configuration
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── README.md           # This file
└── src/
    ├── query.py        # Main script for querying the API
    ├── queries.py      # Predefined queries
    └── config.py       # Configuration management
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
