"""
Main script to query the Perplexity API
"""
import os
from dotenv import load_dotenv
from perplexity import Perplexity

# Load environment variables from .env file
load_dotenv()

def query_perplexity(question: str, preset: str = "pro-search"):
    """
    Query the Perplexity API with a given question.
    
    Args:
        question (str): The question to ask the API
        preset (str): The preset to use (default: "pro-search")
    
    Returns:
        str: The response text from the API
    """
    # Initialize the client (uses PERPLEXITY_API_KEY environment variable)
    client = Perplexity()
    
    # Make the API call with a preset
    response = client.responses.create(
        preset=preset,
        input=question
    )
    
    return response.output_text

if __name__ == "__main__":
    # Example usage
    question = "Who created the broom and what is its historical significance?"
    
    print(f"Question: {question}")
    print("-" * 50)
    
    try:
        result = query_perplexity(question)
        print("Response:")
        print(result)
    except Exception as e:
        print(f"Error: {e}")
