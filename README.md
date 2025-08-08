# 🤖 AI Agent with Gemini

A powerful AI chatbot application built with LangChain, Google's Gemini LLM, and Streamlit. This agent can perform web searches and engage in intelligent conversations with memory capabilities.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-LLM-orange.svg)

## ✨ Features

- 🔍 **Web Search Integration**: Real-time web search using SerpAPI
- 💬 **Conversational Memory**: Maintains context across conversations
- 🎛️ **Multiple Agent Types**: Support for different reasoning approaches
- 📱 **Beautiful UI**: Clean and intuitive Streamlit interface
- 🤖 **Multiple Gemini Models**: Choose between different Gemini model variants
- ⚙️ **Configurable Settings**: Customize agent behavior and parameters

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- SerpAPI key (for web search functionality)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Susandhungana1/Ai-Agent-With-Gemini.git
cd Ai-Agent-With-Gemini
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your_gemini_api_key_here"
SERPAPI_API_KEY="your_serpapi_key_here"
```

5. **Run the application**
```bash
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`

## 🔑 API Keys Setup

### Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### SerpAPI Key
1. Visit [SerpAPI](https://serpapi.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy the key to your `.env` file

## 🎯 Usage

### Basic Chat
- Open the app and navigate to the "Chat" tab
- Type your question in the chat input
- The agent will respond using Gemini's capabilities

### Web Search Queries
Try these example queries:
- "What's the latest news about AI?"
- "Current weather in New York"
- "Latest stock price of Tesla"
- "Recent developments in quantum computing"

### Configuration Options
- **Model Selection**: Choose between Gemini 1.5 Flash, Pro, or 1.0 Pro
- **Agent Types**: Different reasoning approaches
- **Memory**: Enable/disable conversation memory
- **Verbose Mode**: See detailed agent reasoning

## 🏗️ Project Structure

```
Ai-Agent-With-Gemini/
├── src/
│   ├── app.py              # Streamlit web application
│   └── main.py             # Core agent logic
├── .env                    # Environment variables (not in repo)
├── .env.example           # Environment template
├── .gitignore             # Git ignore file
├── requirements.txt        # Python dependencies
├── LICENSE                # License file
└── README.md              # This file
```

## 🛠️ Tech Stack

- **[LangChain](https://langchain.com/)**: Agent framework and orchestration
- **[Google Gemini](https://ai.google.dev/)**: Large language model
- **[SerpAPI](https://serpapi.com/)**: Web search functionality
- **[Streamlit](https://streamlit.io/)**: User interface framework
- **[Python](https://python.org/)**: Programming language

## 🤖 Agent Types

### Zero-shot React Description
- Reasoning and acting without prior examples
- Best for general-purpose queries
- Default and recommended option

### React Docstore
- Document-based reasoning approach
- Useful for information retrieval tasks

### Self-ask with Search
- Breaks down complex questions into simpler parts
- Ideal for multi-step reasoning tasks

## 📊 Models Available

| Model | Description | Use Case |
|-------|-------------|----------|
| `gemini-1.5-flash` | Fast and efficient | Quick responses, general chat |
| `gemini-1.5-pro` | More capable | Complex reasoning, detailed analysis |
| `gemini-1.0-pro` | Original pro model | Stable, reliable performance |

## 🔧 Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY="your_gemini_api_key"
SERPAPI_API_KEY="your_serpapi_key"
```

## 🚨 Security

- **Never commit your `.env` file** to the repository
- Keep your API keys confidential
- Use environment variables for all sensitive data
- Add `.env` to your `.gitignore` file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Susandhungana1/Ai-Agent-With-Gemini/issues) page
2. Create a new issue with detailed description
3. Include error messages and steps to reproduce

## 🚧 Roadmap

- [ ] Add more LLM providers (OpenAI, Anthropic)
- [ ] Implement document upload and analysis
- [ ] Add voice input/output capabilities
- [ ] Create Docker deployment option
- [ ] Add unit tests and CI/CD pipeline

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SerpAPI Documentation](https://serpapi.com/search-api)

## 👨‍💻 Author

**Susandhungana1**
- GitHub: [@Susandhungana1](https://github.com/Susandhungana1)
- Repository: [Ai-Agent-With-Gemini](https://github.com/Susandhungana1/Ai-Agent-With-Gemini)

## 🙏 Acknowledgments

- Google for the Gemini API
- LangChain team for the excellent framework
- Streamlit for the amazing UI framework
- SerpAPI for web search capabilities

---

**Made with ❤️ and Python**