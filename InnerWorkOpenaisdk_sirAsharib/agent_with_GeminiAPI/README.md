# Multi-Agent System with Gemini API

This project demonstrates a multi-agent system built using the Gemini API, featuring specialized agents for different tasks. The system includes a coordinator agent that routes queries to appropriate specialized agents based on the user's intent.

![Open AI SDK Inner Working](assets/image.png)

## Features

- **Coordinator Agent**: Routes user queries to specialized agents
- **Greeting Agent**: Handles welcome messages and greetings
- **Asharib Info Agent**: Provides information about Asharib Ali using his profile API
- **Gemini API Integration**: Utilizes Gemini 1.5 Flash model for enhanced performance

## Prerequisites

- Python 3.8 or higher
- Gemini API key
- Internet connection (for API access)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
3. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

## Project Structure

```
├── main.py           # Main application file containing agent definitions
├── pyproject.toml    # Project configuration
├── README.md         # Project documentation
└── uv.lock          # Dependency lock file
```

## Teacher Video Link

[Inner working of OpenAI Agents SDK](https://www.youtube.com/watch?v=Xkg6JBUFkPY)

## Components

### 1. Coordinator Agent
- Routes user queries to specialized agents
- Analyzes user intent to determine appropriate routing
- Manages handoffs between agents

### 2. Greeting Agent
- Handles welcome messages and greetings
- Responds with "Assalamu Alaikum" and friendly messages

### 3. Asharib Info Agent
- Fetches and provides information about Asharib Ali
- Uses an API endpoint to get real-time profile data
- Handles various queries about Asharib's background, work, and achievements

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Enter your query when prompted
3. The system will:
   - Analyze your query
   - Route to the appropriate agent
   - Provide relevant response

## Example Queries

- Greeting: "Hello" or "Hi"
- Information: "Who is Asharib Ali?" or "What does Asharib do?"

## Error Handling

The system includes robust error handling for:
- API connection issues
- Invalid queries
- Routing errors

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.