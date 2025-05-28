# Chainlit Chatbot with Gemini Integration

A stateful chatbot built with Chainlit and integrated with Google's Gemini AI model through OpenAI-compatible endpoints.

## Features

- Stateful conversation management
- Web-based UI powered by Chainlit
- Integration with Gemini AI model
- Message history tracking
- Async support for better performance

## Prerequisites

- Python 3.13 or higher
- Gemini API key
- Required Python packages (specified in pyproject.toml)

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -e .
```

## Configuration

1. Create a `.env` file in the root directory
2. Add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

Run the chatbot using Chainlit:

```bash
chainlit run main.py
```

The chatbot will be available at `http://localhost:8000`

## Project Structure

- `main.py`: Core application code
- `pyproject.toml`: Project dependencies and metadata
- `.env`: Environment variables (API keys)
- `.gitignore`: Git ignore rules
- `.python-version`: Python version specification

## How It Works

1. The chatbot initializes with Gemini AI configuration
2. Uses Chainlit for the web interface
3. Maintains conversation history for context
4. Processes messages asynchronously
5. Sends responses back through the Chainlit UI

## Dependencies

- chainlit >= 2.5.5
- openai-agents >= 0.0.16
- python-dotenv >= 1.1.0

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.