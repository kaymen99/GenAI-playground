import os, json
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style, init
from litellm import completion
from tavily import TavilyClient

# Load environment variables from a .env file
load_dotenv()

# Initialize colorama for colored terminal output
init(autoreset=True)

# System prompt that defines the behavior and capabilities of the AI agent
system_prompt = f"""
You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!

The current date is: {datetime.now().strftime("%Y-%m-%d")}
"""

# Initialize the Tavily client for searching internet
tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

def search_internet(query: str):
    """
    @notice Searches the internet for the given query.
    @param query The search query.
    @return The combined content from the search results.
    """
    content = ""
    response = tavily.search(query=query, max_results=4)
    for r in response['results']:
        content += r['content']
    return content

class Agent:
    """
    @title AI Agent Class
    @notice This class defines an AI agent that can uses function calling to interact with tools and generate responses.
    """

    def __init__(self, model, tools, available_tools, system_prompt=""):
        """
        @notice Initializes the Agent class.
        @param model The AI model to be used for generating responses.
        @param tools A list of tools that the agent can use.
        @param available_tools A dictionary of available tools and their corresponding functions.
        @param system_prompt system prompt for agent behaviour.
        """
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools
        self.available_tools = available_tools
        self.messages = []
        if self.system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def invoke(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        """
        @notice Executes the AI model to generate a response and handle tool calls if needed.
        @return The final response from the AI.
        """
        # First, call the AI to get a response
        response = self._call_llm()
        response_message = response.choices[0].message
        self.messages.append(response_message)

        try:
            tool_calls = response_message.tool_calls
            if tool_calls:
                response = self._run_tools(tool_calls)
                response_message = response.choices[0].message
        except Exception as e:
            print(Fore.RED + f"Error during tool call: {e}")
            pass
        return response_message.content

    def _run_tools(self, tool_calls):
        """
        @notice Runs the necessary tools based on the tool calls from the AI response.
        @param tool_calls The list of tool calls from the AI response.
        @return The final response from the AI after processing tool calls.
        """
        # For each tool the AI wanted to call, call it and add the tool result to the list of messages
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.available_tools[function_name]
            function_args = json.loads(tool_call.function.arguments)

            print(Fore.GREEN + f"Calling tool: {function_name}")
            print(Fore.GREEN + f"Arguments: {function_args}")
            function_response = function_to_call(**function_args)

            self.messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            })

        # Call the AI again so it can produce a response with the result of calling the tool(s)
        response = self._call_llm()
        response_message = response.choices[0].message
        self.messages.append(response_message)

        # If the AI decided to invoke a tool again, invoke it
        try:
            tool_calls = response_message.tool_calls
            if tool_calls:
                response = self._run_tools(tool_calls)
        except Exception as e:
            print(Fore.RED + f"Error during recursive tool call: {e}")
            pass

        return response

    def _call_llm(self):
        print(Fore.GREEN + "Calling LLM...")
        response = completion(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            temperature=0.1
        )
        return response

# Define the tools that the AI agent can use
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_internet",
            "description": "Search the internet for a given user query, useful to get real time news and information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    },
                },
                "required": ["query"]
            }
        }
    }
]

# Map tool names to their corresponding functions
available_tools = {
    "search_internet": search_internet
}

# Define the model to be used by the agent
model = "groq/llama3-70b-8192"
# model = "gemini/gemini-1.5-flash"

# Create the agent with the specified LLM, tools, and system prompt
agent = Agent(model, tools, available_tools, system_prompt)

def get_response(query):
    result = agent.invoke(query)
    return result

def chat():
    print(Fore.BLUE + "Welcome to the AI Chat! Type 'exit' to end the conversation.")
    while True:
        user_input = input(Fore.RED + "You: ")
        if user_input.lower() == 'exit':
            print(Fore.RED + "AI: Goodbye!")
            break
        response = get_response(user_input)
        print(Fore.RED + f"AI: {response}")

if __name__ == "__main__":
    chat()
