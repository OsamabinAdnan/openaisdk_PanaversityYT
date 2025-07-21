import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (like your API key)
load_dotenv()

# Set the base URL for the OpenRouter API
BASE_URL = "https://openrouter.ai/api/v1/"
# Specify the model to use for the chat completion
MODEL_NAME = "tencent/hunyuan-a13b-instruct:free"

# Retrieve the API key from environment variables
openRouter_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Raise an error if the API key is missing
if not openRouter_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")

# Make a POST request to the OpenRouter chat completions endpoint
response = requests.post(
    url=f"{BASE_URL}chat/completions",
    headers={
        "Authorization": f"Bearer {openRouter_API_KEY}",  # Include the API key in the Authorization header
        "Content-Type": "application/json"  # Specify that the body is JSON
    },
    data=json.dumps({  # Convert the payload to a JSON-formatted string
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": "Hi there! Can you tell me a joke?",  # User's message to the chatbot
            }
        ]
    })
)

# OPTIONAL: Uncomment the lines below to print the full raw JSON response in a pretty format
# pretty_print = json.dumps(response.json(), indent=4)
# print(pretty_print)

# Parse the JSON response into a Python dictionary
data = response.json()

# Extract the chatbot's message from the response
final_response = data['choices'][0]['message']['content']

# Print the chatbot's response in a formatted way
print("\n Response from OpenRouter API: \n")
print("*" * 35)
print(final_response)
