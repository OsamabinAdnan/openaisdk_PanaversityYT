# This script demonstrates how to use LiteLLM to interact with Google's Gemini model.
# LiteLLM provides a unified interface for multiple LLM providers (OpenAI, Anthropic, Gemini, etc.)
# It loads API keys from a .env file and sends a prompt to the Gemini model, printing the response.

import os
from litellm import completion  # Import the LiteLLM completion function
from dotenv import load_dotenv  # For loading environment variables from .env

# Load environment variables from .env file
load_dotenv()

def main():
    # Retrieve the Gemini API key from environment variables
    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    # Uncomment below to use OpenAI or Anthropic keys if needed
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    # Check if the Gemini API key is available
    if not gemini_api_key:
        print("Error: Gemini API key not found in environment variables.")
        return
    
    # Uncomment below to check for other API keys
    # if not openai_api_key:
    #     print("Error: OPENAI_API_KEY not found!")
    #     return
    # if not anthropic_api_key:
    #     print("Error: ANTHROPIC_API_KEY not found!")
    #     return
    
    # Send a prompt to the Gemini model using LiteLLM
    response = completion(
        model="gemini/gemini-1.5-flash",  # Specify the Gemini model
        api_key=gemini_api_key,  # Pass the Gemini API key
        messages=[
            {
                "role": "user",
                "content": "Hello! Please say hello back and tell me one interesting fact about AI."
            },
        ],
        max_tokens=100,      # Limit the response length
        temperature=0.7      # Set randomness of the response
    )

    # Print the model's response in a formatted way
    print("LitLLM Response:")
    print("=" * 40)
    print(response.choices[0].message.content)
    print("=" * 40)
    print(f"Model used : {response.model}")
    # Print token usage if available
    if hasattr(response, "usage") and response.usage:
        print(f"Token used : {response.usage.total_tokens}")

if __name__ == "__main__":
    main()