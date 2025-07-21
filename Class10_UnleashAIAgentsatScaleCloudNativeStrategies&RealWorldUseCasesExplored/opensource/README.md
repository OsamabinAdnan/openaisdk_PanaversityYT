# OpenRouter API Integration Examples

This repository demonstrates two different methods of integrating with the OpenRouter API, which provides access to various AI models through a unified interface.

## Overview

The project contains two implementation approaches:
1. Direct REST API Method (`Direct_Method.py`)
2. OpenAI SDK Method with Agents (`OpenAISDK_Method.py`)

## Prerequisites

- Python 3.7+
- OpenRouter API key (set in `.env` file)
- Required Python packages (install via pip):
  ```
  python-dotenv
  requests
  openai
  agents
  ```

## Implementation Methods

### 1. Direct REST API Method

`Direct_Method.py` shows how to interact with OpenRouter API directly using HTTP requests:
- Uses the `requests` library for HTTP communication
- Makes direct POST requests to OpenRouter's chat completions endpoint
- Simple and straightforward implementation
- Good for basic use cases

### 2. OpenAI SDK Method with Agents

`OpenAISDK_Method.py` demonstrates a more sophisticated approach:
- Uses the official OpenAI SDK with async support
- Implements an agent-based architecture
- Supports asynchronous operations
- Provides more structured and scalable solution
- Includes custom agent framework integration

## Environment Setup

1. Create a `.env` file in the root directory
2. Add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   ```

## Available Models

Both implementations showcase the use of different free models available through OpenRouter:
- Direct Method uses: `tencent/hunyuan-a13b-instruct:free`
- SDK Method uses: `deepseek/deepseek-r1-0528-qwen3-8b:free`

You can explore more available free models at: [OpenRouter Models](https://openrouter.ai/models?fmt=table&max_price=0)

## Documentation Links

- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [OpenAI SDK Documentation](https://github.com/openai/openai-python)

## Usage

### Direct Method
```python
python Direct_Method.py
```

### SDK Method with Agents
```python
python OpenAISDK_Method.py
```

## Features

- Environment variable support
- Error handling for missing API keys
- Configurable model selection
- Response formatting
- Async support (in SDK method)
- Agent-based architecture (in SDK method)

## Note

Make sure to check OpenRouter's documentation for:
- Latest model availability
- Pricing information
- API limits and quotas
- Best practices
