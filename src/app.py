import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.utilities import SerpAPIWrapper
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Agent with Gemini",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .agent-message {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
    }
    .sidebar-content {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'agent_initialized' not in st.session_state:
    st.session_state.agent_initialized = False
if 'memory' not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("🔧 Configuration")
    
    # API Key status
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    
    if gemini_api_key:
        st.success("✅ Gemini API Key loaded")
    else:
        st.error("❌ Gemini API Key not found")
    
    if serpapi_key:
        st.success("✅ SerpAPI Key loaded")
    else:
        st.error("❌ SerpAPI Key not found")
    
    st.divider()
    
    # Agent settings
    st.header("🤖 Agent Settings")
    model_choice = st.selectbox(
        "Gemini Model",
        ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
        index=0
    )
    
    agent_type = st.selectbox(
        "Agent Type",
        ["zero-shot-react-description", "react-docstore", "self-ask-with-search"],
        index=0
    )
    
    verbose_mode = st.checkbox("Verbose Mode", value=True)
    use_memory = st.checkbox("Use Conversation Memory", value=True)
    
    st.divider()
    
    # Clear conversation
    if st.button("🗑️ Clear Conversation", type="secondary"):
        st.session_state.conversation_history = []
        st.session_state.memory = ConversationBufferMemory()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">🤖 AI Agent with Gemini</h1>', unsafe_allow_html=True)

# Initialize the agent
@st.cache_resource
def initialize_ai_agent(_model_choice):  # Add underscore prefix to avoid caching issues
    try:
        # Initialize the Gemini LLM with the selected model
        llm = ChatGoogleGenerativeAI(
            model=_model_choice,
            google_api_key=gemini_api_key,
            temperature=0.7
        )
        
        # Initialize tools with SerpAPI key
        search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
        tools = [Tool(name="Search", func=search.run, description="Search the web for information.")]
        
        return llm, tools
    except Exception as e:
        st.error(f"Error initializing agent: {str(e)}")
        return None, None

# Get LLM and tools
llm, tools = initialize_ai_agent(model_choice)

if llm and tools:
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Examples", "📖 About"])
    
    with tab1:
        st.subheader("Chat with AI Agent")
        
        # Display conversation history
        for i, (user_msg, agent_msg) in enumerate(st.session_state.conversation_history):
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>🧑 You:</strong> {user_msg}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="chat-message agent-message">
                <strong>🤖 Agent:</strong> {agent_msg}
            </div>
            """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Ask me anything...")
        
        if user_input:
            with st.spinner("🤔 Agent is thinking..."):
                try:
                    # Initialize agent with current settings
                    if use_memory:
                        agent = initialize_agent(
                            tools, 
                            llm, 
                            agent=agent_type, 
                            memory=st.session_state.memory,
                            verbose=verbose_mode
                        )
                    else:
                        agent = initialize_agent(
                            tools, 
                            llm, 
                            agent=agent_type, 
                            verbose=verbose_mode
                        )
                    
                    # Get response
                    response = agent.run(user_input)
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append((user_input, response))
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab2:
        st.subheader("📊 Example Queries")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔍 Search Queries")
            examples_search = [
                "What is the latest news about AI?",
                "Current weather in New York",
                "Latest stock price of Tesla",
                "Recent developments in quantum computing"
            ]
            
            for example in examples_search:
                if st.button(f"Try: {example}", key=f"search_{example}"):
                    st.session_state.example_query = example
        
        with col2:
            st.markdown("### 💭 General Queries")
            examples_general = [
                "Explain quantum physics in simple terms",
                "What are the benefits of renewable energy?",
                "How does machine learning work?",
                "Tell me about the history of the internet"
            ]
            
            for example in examples_general:
                if st.button(f"Try: {example}", key=f"general_{example}"):
                    st.session_state.example_query = example
        
        # Process example query
        if hasattr(st.session_state, 'example_query'):
            example_query = st.session_state.example_query
            del st.session_state.example_query
            
            with st.spinner("🤔 Processing example query..."):
                try:
                    agent = initialize_agent(tools, llm, agent=agent_type, verbose=verbose_mode)
                    response = agent.run(example_query)
                    st.session_state.conversation_history.append((example_query, response))
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with tab3:
        st.subheader("📖 About This App")
        
        st.markdown("""
        ### 🤖 AI Agent with Gemini
        
        This application demonstrates the power of LangChain agents combined with Google's Gemini LLM.
        
        **Features:**
        - 🔍 Web search capabilities using SerpAPI
        - 💬 Conversational memory
        - 🎛️ Configurable agent types
        - 📱 Beautiful Streamlit interface
        
        **How it works:**
        1. The agent receives your query
        2. Determines if web search is needed
        3. Uses available tools to gather information
        4. Provides a comprehensive response
        
        **Agent Types:**
        - **Zero-shot React**: Reasoning and acting without examples
        - **React Docstore**: Document-based reasoning
        - **Self-ask with Search**: Decomposition of complex questions
        
        ### 🛠️ Tech Stack
        - **LangChain**: Agent framework
        - **Gemini**: Google's large language model
        - **SerpAPI**: Web search functionality
        - **Streamlit**: User interface
        """)
        
        st.divider()
        
        # System status
        st.subheader("🔧 System Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("API Status", "✅ Connected" if gemini_api_key else "❌ Disconnected")
        
        with col2:
            st.metric("Tools Available", len(tools) if tools else 0)
        
        with col3:
            st.metric("Conversations", len(st.session_state.conversation_history))

else:
    st.error("⚠️ Failed to initialize AI agent. Please check your API configuration.")
    st.info("Make sure your Gemini API key and SerpAPI key are properly set in the .env file.")