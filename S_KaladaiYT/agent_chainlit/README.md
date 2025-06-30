# Chainlit Multi-Agent Assistant

This project implements a multi-agent assistant using [Chainlit](https://www.chainlit.io/) and a Gemini-powered OpenAI-compatible API. The assistant is designed to help users with frontend, backend, animation, and SEO development tasks by delegating work to specialized expert agents, all coordinated by a manager agent.

## Live Demo Link

[Developer Agent](https://developeragent-assistant.up.railway.app/)

## Features

- **Frontend Expert Agent**: Specializes in frontend development (React, Angular, Next.js, Vue.js).
- **Backend Expert Agent**: Specializes in backend development (Node.js, Python, Ruby on Rails, Java).
- **Animation Expert Agent**: Specializes in web animations (CSS, JavaScript, Framer Motion, Three.js, GSAP, Anime.js).
- **SEO Expert Agent**: Specializes in SEO optimization (keyword optimization, meta tags, structured data, best practices).
- **Manager Agent**: Delegates tasks to the appropriate expert agent and coordinates the workflow.
- **Chat Interface**: Users interact with the assistant via a chat interface powered by Chainlit.

## How It Works

1. **User starts a chat**: The assistant greets the user and initializes a conversation history.
2. **User sends a message**: The message is added to the conversation history.
3. **Manager Agent**: Receives the conversation history and delegates tasks to the appropriate expert agent(s).
4. **Expert Agents**: Generate responses based on their domain expertise.
5. **Response**: The assistant's response is sent back to the user and added to the conversation history.

## Setup Instructions

### Prerequisites
- Python 3.8+
- [Chainlit](https://www.chainlit.io/) installed (`pip install chainlit`)
- [python-dotenv](https://pypi.org/project/python-dotenv/) installed (`pip install python-dotenv`)
- Gemini API key (set as `GEMINI_API_KEY` in your `.env` file)

### Installation

1. **Clone the repository**
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
   Or use `pyproject.toml` if using Poetry or similar tools.
3. **Set up environment variables**:
   - Create a `.env` file in the project root:
     ```env
     GEMINI_API_KEY=your_gemini_api_key_here
     ```
4. **Run the app**:
   ```sh
   chainlit run main.py
   ```

## File Structure

- `main.py` - Main application file containing agent definitions and event handlers.
- `README.md` - Project documentation.
- `pyproject.toml` - Project metadata and dependencies (if using Poetry).
- `Procfile` - For deployment (e.g., on Heroku).
- `.env` - Environment variables (not included in repo).

## Usage

- Start the Chainlit app and open the provided URL in your browser.
- Interact with the assistant by describing your development needs.
- The assistant will respond with expert advice or solutions, leveraging the appropriate agent(s).

## License

This project is for educational and demonstration purposes.
