import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.utilities import SerpAPIWrapper
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Retrieve the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini LLM with the correct import
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=gemini_api_key,
    temperature=0.7
)

prompt = "What is the capital of France?"

search = SerpAPIWrapper()
tools = [Tool(name="Search", func=search.run, description="Search the web for information.")]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("What is the latest news about AI?")

memory = ConversationBufferMemory()
agent_with_memory = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory, verbose=True
)