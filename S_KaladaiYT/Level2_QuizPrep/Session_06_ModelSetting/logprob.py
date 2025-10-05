from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Request completion with logprobs
response = client.completions.create(
    model="gpt-3.5-turbo-instruct", # Logprobs works on instruct models, not chat models
    prompt="Explain Agenti AI shortly, upto 3 lines.",
    logprobs=5,  # Request log probabilities for the top 5 tokens
)

# Print token with logprobs
for choice in response.choices:
    for token, logprob in zip(choice.logprobs.tokens, choice.logprobs.token_logprobs):
        print(f"Token: {token}, Logprob: {logprob}")