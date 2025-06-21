# AI Assistant with Agents SDK and Chainlit

This project implements an AI assistant using the Agents SDK integrated with Chainlit for a chat interface. The assistant uses the Gemini 2.0 Flash model through a custom OpenAI-compatible endpoint.

## Features

- Interactive chat interface powered by Chainlit
- Integration with Gemini 2.0 Flash model
- Asynchronous message handling
- Environment variable configuration
- Custom OpenAI-compatible client implementation

## Prerequisites

Before running this project, make sure you have:

1. Python installed on your system
2. Gemini API key
3. Required Python packages (specified in pyproject.toml)

## Installation

1. Clone the repository
2. Create a `.env` file in the root directory with:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To start the chat interface:

```bash
chainlit run main.py
```

The application will start a local server, and you can interact with the AI assistant through your web browser.

## Project Structure

- `main.py`: Main application file containing the chat implementation
- `.env`: Environment variables configuration
- `pyproject.toml`: Project dependencies and configuration

## Implementation Details

The project uses:
- `Agent` class for AI assistant behavior definition
- `AsyncOpenAI` for API communication
- `OpenAIChatCompletionsModel` for model configuration
- `RunConfig` for execution settings
- Chainlit decorators for handling chat events

## Environment Variables

Required environment variables:
- `GEMINI_API_KEY`: Your Gemini API key

## Error Handling

The application includes basic error handling:
- Checks for missing API key
- Asynchronous error handling in chat operations

## Contributing

Feel free to open issues and pull requests for any improvements.
