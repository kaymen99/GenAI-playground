# AI Researcher Agent Project

In this project I showcase different techniques that can be used for building AI agents, i used as an example a researcher agent. The project includes three scripts: building an AI agent from scratch with Python, using Langgraph to develop a graph-based agent for scratch, and creating a ReAct agent with the Langgraph `create_react_agent` method. Each script demonstrates integration with various LLMs and tools, using the Tavily API for real-time internet searches.

## Table of Contents
- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Tools and Libraries](#tools-and-libraries)

## Project Structure

### AI Agent from Scratch
The `ai_agent_from_scratch` script builds an AI agent from scratch using Python. It leverages the `litellm` library to integrate with various language models (LLMs) such as OpenAI, Gemini, and GROQ. The `litellm` library provides a standard LLM completion API, allowing calls to 100+ LLMs using the same Input/Output format used by openai.

### AI Agent with Langgraph
The `ai_agent_langgraph` script uses `langgraph` to build an AI agent in a graph manner. The graph consists of an LLM and tools. Interaction with the graph involves:
1. Calling the agent (LLM) to decide if tools should be used.
2. Running tools and passing results back to the agent if needed.
3. Finishing the response if no tools are required.

The script uses Llama3 with GROQ as the LLM, with commented code to optionally use Google Gemini.

### React Agent with Langgraph
The `react_agent_langgraph` script is a simplified version of the ReAct agent built with Langchain from scratch. Langgraph's new method `create_react_agent` allows for creating the agent in a single line, simplifying message history management and enabling multiple users' interaction with threads.

### Tavily Search API
All scripts utilize the Tavily API for searching the internet. Tavily Search API is optimized for LLMs, providing a factual, efficient, and persistent search experience.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/kaymen99/GenAI-playground.git
   cd GenAI-playground/ai-agents
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file and add your API keys:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

## Usage
1. Choose the script you want to run:
   - `ai_agent_from_scratch.py`
   - `ai_agent_langgraph.py`
   - `react_agent_langgraph.py`

2. Run the chosen script:
   ```bash
   python ai_agent_from_scratch.py
   ```

3. Start chatting with the AI agent in the terminal.

## Tools and Libraries
- [litellm](https://github.com/your-username/litellm): Provides a standard LLM completion API.
- [Langgraph](https://github.com/your-username/langgraph): Enables building AI agents in a graph manner.
- [Tavily API](https://tavily.com/): Search engine optimized for LLMs.
