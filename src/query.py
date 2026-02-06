"""Main script to query the Perplexity API from the command line."""
import os
import sys
from dotenv import load_dotenv
from perplexity import Perplexity
# Import session safely so the script can be run as a module or a plain script
try:
    from .session import QueryClient
except Exception:
    from session import QueryClient

# Load environment variables from .env file when running locally
load_dotenv()


def query_perplexity(question: str, preset: str = None, session_path: str = None) -> str:
    """Query the Perplexity API with a given question while keeping chat memory.

    Uses `QueryClient` which persists a small conversation history to `session_path`.
    """
    if preset is None:
        preset = os.getenv("PERPLEXITY_PRESET", "sonar")

    client = QueryClient(preset=preset, state_path=session_path)
    return client.query(question)


def main():
    # Accept the prompt from command-line arguments, or use stdin if piped
    if not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    elif len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = os.getenv("PERPLEXITY_PROMPT", "What are the latest developments in AI?")

    if not prompt:
        print("No prompt provided.")
        sys.exit(2)

    print(f"Question: {prompt}\n{'-' * 50}")

    try:
        # default session file in current working directory
        session_file = os.getenv("PERPLEXITY_SESSION_PATH")
        result = query_perplexity(prompt, session_path=session_file)
        print("Response:\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
