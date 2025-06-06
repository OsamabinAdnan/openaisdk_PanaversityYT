# OpenAI Agent SDK Demo - Greeting Agent

This project demonstrates the implementation of a simple AI agent using the OpenAI SDK. The agent is designed to respond to greetings with appropriate responses, specifically saying "salam" when users greet it.

## Features

- Custom AI agent implementation using OpenAI SDK
- Simple greeting response system
- Environment variable support for secure API key management
- Synchronous execution of AI agent

## Prerequisites

Before running this project, make sure you have:

1. Python installed on your system
2. OpenAI API key
3. Required Python packages (see Installation section)

## Installation

1. Clone this repository
2. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
3. Install the required dependencies:
   ```
   pip install python-dotenv
   ```

## Project Structure

- `main.py`: Main application file containing the greeting agent implementation
- `.env`: Environment variables file (you need to create this)
- `README.md`: Project documentation
- `pyproject.toml`: Project dependencies and configuration
- `uv.lock`: Lock file for dependencies

## Usage

1. Run the main script:
   ```
   python main.py
   ```
2. Enter your greeting when prompted
3. The agent will respond with an appropriate greeting

## Code Overview

The project uses two main classes from the OpenAI SDK:

- `Agent`: Defines the AI agent's behavior and capabilities
- `Runner`: Executes the agent and manages its responses

The greeting agent is configured with:
- A specific name ("Greeting Agent")
- Custom instructions for handling greetings
- No special tools or handoffs (keeping it simple)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open-source and available under the MIT License.

## Note

Remember to keep your OpenAI API key secure and never commit it to version control.