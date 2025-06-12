# This script demonstrates the usage of OpenRouter, a unified API gateway for various AI models.
# OpenRouter provides access to multiple AI models through a single API interface.
# It loads the API key from a .env file and sends a prompt to a selected model, printing the response.

import os
from openai import OpenAI  # Using OpenAI's client with custom base URL
from dotenv import load_dotenv  # For loading environment variables from .env

# Load environment variables from .env file
load_dotenv()

def main():
    # Get OpenRouter API key from environment variables
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    print(openrouter_api_key)

    # Check if API key is present
    if not openrouter_api_key:
        print("Error: OpenRouter API key not found in environment variables.")
        return
    
    # Initialize OpenAI client with OpenRouter's base URL
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",  # OpenRouter API endpoint
        api_key=openrouter_api_key,
    )

    # Get user input for the conversation
    user_input = input("Enter your question:")

    # Make an API call to OpenRouter
    response = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",  # Using DeepSeek's free model
        messages=[
            {
                "role": "user",
                "content": user_input,
            },
        ],
        max_tokens=200,  # Maximum number of tokens in the response
        
    )

    # Print the response in a formatted way
    print("OpenRouter Response:")
    print("=" * 40)
    print(response.choices[0].message.content)
    print("=" * 40)
    print(f"Model used: {response.model}")
    print(f"Token used: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()