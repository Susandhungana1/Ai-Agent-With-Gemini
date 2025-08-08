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

# Enhanced CSS for better dark mode support
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #2196f3, #9c27b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Chat message base styling */
    .chat-message {
        padding: 1rem 1.2rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        display: block;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        line-height: 1.5;
        position: relative;
    }
    
    /* User message - chat bubble style */
    .user-message {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.15), rgba(33, 150, 243, 0.08));
        border-left: none;
        border: 1px solid rgba(33, 150, 243, 0.2);
        border-radius: 1rem 1rem 0.2rem 1rem;
        margin-left: auto;
    }
    
    /* Agent message - chat bubble style */
    .agent-message {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.15), rgba(156, 39, 176, 0.08));
        border-left: none;
        border: 1px solid rgba(156, 39, 176, 0.2);
        border-radius: 1rem 1rem 1rem 0.2rem;
        margin-right: auto;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Dark mode chat bubbles */
    .stApp[data-theme="dark"] .user-message {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.3), rgba(33, 150, 243, 0.2)) !important;
        border-color: rgba(33, 150, 243, 0.4) !important;
    }
    
    .stApp[data-theme="dark"] .agent-message {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.3), rgba(156, 39, 176, 0.2)) !important;
        border-color: rgba(156, 39, 176, 0.4) !important;
    }
    
    /* Light mode chat bubbles */
    .stApp[data-theme="light"] .user-message {
        background: linear-gradient(135deg, rgba(33, 150, 243, 0.12), rgba(33, 150, 243, 0.06)) !important;
        border-color: rgba(33, 150, 243, 0.25) !important;
    }
    
    .stApp[data-theme="light"] .agent-message {
        background: linear-gradient(135deg, rgba(156, 39, 176, 0.12), rgba(156, 39, 176, 0.06)) !important;
        border-color: rgba(156, 39, 176, 0.25) !important;
    }
    
    /* Chat container styling */
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 1rem 0;
    }
    
    /* Responsive chat bubbles */
    @media (max-width: 768px) {
        .chat-message {
            max-width: 90% !important;
            padding: 0.8rem 1rem;
        }
        
        .main-header {
            font-size: 2rem;
        }
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
        
        # Create a container for the chat messages
        chat_container = st.container()
        
        with chat_container:
            # Display conversation history with better layout
            for i, (user_msg, agent_msg) in enumerate(st.session_state.conversation_history):
                # User message - aligned to the right
                col1, col2 = st.columns([1, 4])
                with col2:
                    st.markdown(f"""
                    <div class="chat-message user-message" style="margin-left: auto; max-width: 80%; text-align: left;">
                        <strong>🧑 You:</strong><br>
                        <span style="margin-top: 0.5rem; display: block; word-wrap: break-word; white-space: pre-wrap;">{user_msg}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Agent message - aligned to the left
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div class="chat-message agent-message" style="max-width: 80%; text-align: left;">
                        <strong>🤖 Agent:</strong><br>
                        <span style="margin-top: 0.5rem; display: block; word-wrap: break-word; white-space: pre-wrap;">{agent_msg}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add some spacing between conversation pairs
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Chat input at the bottom
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