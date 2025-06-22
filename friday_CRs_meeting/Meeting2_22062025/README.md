# Multi-Language Weather Assistant

This project implements a multi-language AI assistant system that can provide weather information in different languages using the Gemini API. The system demonstrates the use of multiple specialized agents working together to handle language-specific requests.

## Features

- Multiple language support (Spanish and French)
- Weather information retrieval
- Intelligent request routing through a triage system
- Async operation for better performance

## Prerequisites

- Python 3.7+
- Gemini API key
- Required Python packages (see `pyproject.toml`)

## Setup

1. Clone the repository
2. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
3. Install dependencies from `pyproject.toml`

## Project Structure

The main components of the system are:

### Agents

1. **Triage Agent**: The main coordinator that analyzes requests and routes them to appropriate language agents
2. **Spanish Agent**: Handles Spanish language responses
3. **French Agent**: Handles French language responses

### Tools

- `getweather`: A mock function that simulates weather information retrieval for any city

## Configuration

The system uses the following configurations:

- **Model**: gemini-2.0-flash
- **API Base URL**: https://generativelanguage.googleapis.com/v1beta/openai/
- Tracing is disabled by default

## Usage

Run the script with:

```bash
python main.py
```

The demo will execute a weather query for Karachi in Spanish, demonstrating:
- Agent handoff
- Weather tool usage
- Multi-language response generation

## Output Format

The script outputs:
- The final response
- The last agent that handled the request
- The name of the last tool called

## Error Handling

The script includes basic error handling for:
- Missing API key validation
- Environment variable checks

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is open-source and available under the MIT License.