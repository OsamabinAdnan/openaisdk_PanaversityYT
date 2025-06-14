# Import required libraries and modules
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is set in your environment variables")

# Initialize the OpenAI client with Gemini configuration
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Set up the language model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

# Configure the runner with the model and client
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True,)

def display_language_menu():
    """
    Display a menu of available languages and get user selection.
    Returns:
        str: The selected language name
    """
    # Dictionary of supported languages with their corresponding menu numbers
    languages = {
        1: "Urdu",
        2: "French",
        3: "Spanish",
        4: "German",
        5: "Chinese (Mandarin)",
        6: "Japanese",
        7: "Korean",
        8: "Arabic",
        9: "Portuguese",
        10: "Russian",
        11: "Hindi",
        12: "Bengali",
        13: "Turkish",
        14: "Italian",
        15: "Dutch",
        16: "Greek",
        17: "Hebrew",
        18: "Malay",
        19: "Czech",
        20: "Romanian",
        21: "Finnish",
        22: "Polish",
        23: "Swedish",
        24: "Danish",
        25: "Norwegian",
        26: "Thai",
        27: "Vietnamese",
    }
    
    # Display the menu header
    print("\n=== Language Translation Menu ===")
    # Print all available languages with their corresponding numbers
    for key, value in languages.items():
        print(f"{key}. {value}")
    
    # Input validation loop
    while True:
        try:
            # Get user's language choice
            choice = int(input("\nSelect target language (1-27): "))
            # Validate the input range
            if 1 <= choice <= 27:
                return languages[choice]
            else:
                print("Please enter a number between 1-27.")
        except ValueError:
            print("Please enter a valid number.")

# Display application header
print("\n=== AI Language Translator ===")
# Get the text to translate from user
user_input = input("Enter text to translate: ")
# Get the target language using the menu function
target_language = display_language_menu()

# Initialize the translator agent with specific instructions
translator_agent = Agent(
    name="Translator Agent",
    instructions=f"""
    You are a professional translator agent. Your task is to translate the given text into {target_language}.
    Please provide an accurate and natural-sounding translation that maintains the original meaning and context.
    Only respond with the translation, no additional explanations needed.
    """,
)

# Indicate translation is in progress
print("\nTranslating...")
# Execute the translation using the Runner
response = Runner.run_sync(
    translator_agent,
    input=user_input,
    run_config=config,
)

# Format and display the translation result
print(f"\nTranslation to {target_language}:")
print("-" * 40)  # Add a separator line
print(response.final_output)
print("-" * 40)  # Add a closing separator line