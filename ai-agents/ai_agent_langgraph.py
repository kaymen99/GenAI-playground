import os
import operator
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Load environment variables from a .env file
load_dotenv()

# Initialize colorama for colored terminal output
init(autoreset=True)

class AgentState(TypedDict):
    """
    @notice Typed dictionary to represent the state of the agent.
    @dev Contains a list of messages.
    """
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:
    """
    @title AI Agent Class
    @notice This class defines an AI agent that can interact with tools and generate responses.
    @dev Uses a state graph to manage interactions between the agent and tools.
    """

    def __init__(self, model, tools, system=""):
        """
        @notice Initializes the Agent class.
        @param model The AI model to be used for generating responses.
        @param tools A list of tools that the agent can use.
        @param system Optional system prompt for the agent behaviour.
        """
        self.system = system
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
        self.messages = []
        if self.system:
            self.messages.append(SystemMessage(content=self.system))
        
        # Build the state graph
        graph = StateGraph(AgentState)

        # Define nodes in the graph
        graph.add_node("llm", self.invoke_llm)
        graph.add_node("tool", self.call_tool)
        
        # Define edges in the graph
        graph.set_entry_point("llm")
        graph.add_edge("tool", "llm")
        graph.add_conditional_edges(
            "llm",
            self.need_tool_call,
            {True: "tool", False: END}
        )
        self.graph = graph.compile()
    
    def need_tool_call(self, state: AgentState):
        """
        @notice Checks if a tool call is needed based on the state.
        @param state The current state of the agent.
        @return True if a tool call is needed, False otherwise.
        """
        print(Fore.GREEN + "Checking if needs tool call...")
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def invoke_llm(self, state: AgentState):
        """
        @notice Invokes the language model to generate a response.
        @param state The current state of the agent.
        @return A dictionary containing the new state with the LLM's response.
        """
        print(Fore.GREEN + "Calling model...")
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        self.messages.append(message)
        return {'messages': [message]}

    def call_tool(self, state: AgentState):
        """
        @notice Calls the necessary tools based on the state.
        @param state The current state of the agent.
        @return A dictionary containing the new state with the tool responses.
        """
        print(Fore.GREEN + "Calling tools...")
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(Fore.GREEN + f"Calling: {t['name']}")
            if not t['name'] in self.tools:      
                result = "bad tool name, retry"  # Instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        self.messages = state['messages'] + results
        return {'messages': results}

# Prompt that defines the behavior and capabilities of the AI agent
agent_prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

# Initialize the AI model (llama3 with Groq)
llama3 = ChatGroq(model="llama3-70b-8192")

# Uncomment and use the following line if you want to use the Gemini model from Google Generative AI
# gemini = ChatGoogleGenerativeAI(model="gemini/gemini-1.5-pro-latest")

# Initialize the search tool (Tavily)
tool = TavilySearchResults(max_results=4)

# Create the agent with the specified LLM, tools, and agent prompt
agent = Agent(llama3, [tool], agent_prompt)

def get_response(query):
    messages = [HumanMessage(content=query)]
    result = agent.graph.invoke({"messages": messages})
    return result["messages"][-1].content

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
