"""Main script to query the Perplexity API from the command line."""
import os
import sys
from dotenv import load_dotenv
from perplexity import Perplexity

# Load environment variables from .env file when running locally
load_dotenv()


def query_perplexity(question: str, preset: str = None) -> str:
    """Query the Perplexity API with a given question.

    Uses the `PERPLEXITY_API_KEY` environment variable for auth.
    """
    if preset is None:
        preset = os.getenv("PERPLEXITY_PRESET", "pro-search")

    client = Perplexity()
    response = client.responses.create(preset=preset, input=question)
    return getattr(response, "output_text", str(response))


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
        result = query_perplexity(prompt)
        print("Response:\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
