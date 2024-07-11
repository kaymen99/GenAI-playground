from langchain_core.messages import SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint import MemorySaver
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Load environment variables from a .env file
load_dotenv()

# Initialize colorama for colored terminal output
init(autoreset=True)

# Prompt that defines the behavior and capabilities of the AI agent
agent_prompt = """You are a smart research assistant. Use the search engine to look up information. \
You are allowed to make multiple calls (either together or in sequence). \
Only look up information when you are sure of what you want. \
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""

# Initialize the AI model (ChatGroq with llama3 model)
llama3 = ChatGroq(model="llama3-70b-8192")

# Uncomment and use the following line if you want to use the Gemini model from Google Generative AI
# gemini = ChatGoogleGenerativeAI(model="gemini/gemini-1.5-pro-latest")

# Initialize the search tool (TavilySearchResults)
search_tool = TavilySearchResults()
tools = [search_tool]

# Initialize memory saver for the agent
memory = MemorySaver()

# Create the react agent with the specified LLM, tools, agent prompt, and memory
app = create_react_agent(llama3, tools, messages_modifier=agent_prompt, checkpointer=memory)

# Configuration for the agent (e.g., specifying thread ID)
config = {"configurable": {"thread_id": "test-thread"}}

# get a response from the AI agent based on user query
def get_response(query):
    # Invoke the AI agent with the user's query and configuration
    messages = app.invoke({"messages": [("user", query)]}, config)
    # Return the content of the last message in the response
    return messages["messages"][-1].content

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
