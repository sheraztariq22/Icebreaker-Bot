# LinkedIn Icebreaker Bot 🤝

An AI-powered assistant that generates personalized icebreakers and conversation starters based on LinkedIn profiles. Built with **Google Gemini AI** and **LlamaIndex**, it helps make professional introductions more personal and engaging.

## 🌟 Features

- **LinkedIn Profile Analysis**: Extract professional data using ProxyCurl API or use mock data
- **AI-Powered Insights**: Generate interesting facts about a person's career/education using Google Gemini
- **Personalized Q&A**: Answer specific questions about the person's background with context-aware responses
- **Multiple AI Models**: Choose between Gemini 2.5 Flash (fast & efficient) or Pro (highest quality)
- **Two Interfaces**: Command-line tool for quick usage and web UI for user-friendly interaction
- **Flexible**: Use mock data for practice or connect to real LinkedIn profiles
- **Free Tier Available**: Get started with Gemini's free tier (1,500 requests/day)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+, < 3.13
- A Google Gemini API key (free - see setup below)
- A ProxyCurl API key (optional - mock data available)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/sheraztariq22/Icebreaker-Bot.git
cd Icebreaker-Bot
```

2. **Create a virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Get your free Gemini API key:**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your key

5. **Configure environment variables:**
```bash
# Create .env file in project root
cp .env.example .env

# Edit .env and add your keys:
# GEMINI_API_KEY=your_gemini_api_key_here
# PROXYCURL_API_KEY=your_proxycurl_key_here  # Optional
```

### Quick Test

Verify your setup works:

```bash
python test_gemini.py
```

You should see:
```
✓ All tests passed! Your migration is successful.
```

## 💻 Usage

### Using the Web Interface (Recommended)

Launch the web app:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

**Web Interface Features:**
- 🔍 **Process Tab**: Enter a LinkedIn URL or use mock data
- 💬 **Chat Tab**: Ask questions about the processed profile
- 🎯 **Model Selection**: Choose between different Gemini models
- 📊 **Real-time Processing**: See facts generated instantly

### Using the Command Line Interface

Run the bot using the terminal:

```bash
# Use mock data (no ProxyCurl API key needed)
python main.py --mock

# Use a real LinkedIn profile
python main.py --url "https://www.linkedin.com/in/username/"

# Use a specific Gemini model
python main.py --mock --model "gemini-2.5-pro"
```

## 🧠 How It Works

The Icebreaker Bot uses a Retrieval-Augmented Generation (RAG) pipeline:

1. **Data Extraction**: LinkedIn profile data is retrieved via ProxyCurl API or mock data
2. **Text Processing**: Profile data is split into manageable chunks (512 tokens each)
3. **Vector Embedding**: Text chunks are converted to vector embeddings using Google's Text Embedding 004 model
4. **Storage**: Embeddings are stored in a vector database for efficient retrieval
5. **Query & Generation**: When asked a question:
   - Relevant profile sections are retrieved using semantic search
   - Google Gemini LLM generates contextually accurate responses
   - Results are returned in natural language

## 🛠️ Project Structure

```
icebreaker_bot/
├── requirements.txt              # Project dependencies
├── config.py                     # Configuration settings (Gemini API, models, prompts)
├── .env                          # Environment variables (API keys)
├── .env.example                  # Template for environment setup
├── test_gemini.py               # Test script to verify setup
├── modules/
│   ├── __init__.py
│   ├── data_extraction.py        # LinkedIn profile data extraction
│   ├── data_processing.py        # Data splitting and vector indexing
│   ├── llm_interface.py          # Gemini LLM setup and interaction
│   └── query_engine.py           # Query processing and response generation
├── app.py                        # Gradio web interface
├── main.py                       # CLI application
└── README.md                     # This file
```

## 🤖 Available Models

### For Chat/Generation:

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| **gemini-2.5-flash** ⭐ | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ High | 💰 Low | **Recommended** - Best for most use cases |
| **gemini-2.5-pro** | ⚡⚡ Medium | ⭐⭐⭐⭐⭐ Highest | 💰💰💰 High | Complex analysis, highest quality needed |
| **gemini-1.5-flash** | ⚡⚡⚡ Fast | ⭐⭐⭐ Good | 💰 Low | Previous generation |
| **gemini-1.5-pro** | ⚡⚡ Medium | ⭐⭐⭐⭐ Very High | 💰💰 Medium | Previous generation Pro |

### For Embeddings:
- **models/text-embedding-004** (Latest, recommended)
- Free to use, 768-dimensional embeddings

**Free Tier Limits:**
- 15 requests per minute
- 1,500 requests per day
- 1M tokens per minute

Perfect for development and small-scale use!

## 📝 Examples

Here are some example questions you can ask:

**Career Questions:**
- "What is this person's current job title?"
- "How long have they been working at their current company?"
- "What was their career progression?"
- "What companies have they worked for?"

**Skills & Education:**
- "What skills do they have related to machine learning?"
- "Where did they get their education?"
- "What certifications do they have?"

**Networking:**
- "What's an interesting icebreaker I could use?"
- "What topics should I discuss with them?"
- "What are their main areas of expertise?"
- "Give me 3 interesting facts about this person"

## 🎨 Customization

### Switching Models

**In Web Interface:**
Use the dropdown menu to select different models

**In CLI:**
```bash
python main.py --mock --model "gemini-2.5-pro"
```

**In Code (config.py):**
```python
# Change the default model
LLM_MODEL_ID = "gemini-2.5-flash"  # or "gemini-2.5-pro"

# Adjust generation parameters
LLM_TEMPERATURE = 0.7  # 0.0 = deterministic, 1.0 = creative
MAX_TOKENS = 1024      # Maximum response length
```

### Customizing Prompts

Edit the prompt templates in `config.py` to change response style:

```python
INITIAL_FACTS_TEMPLATE = """Context information is below.
---------------------
{context_str}
---------------------
Given the context information, provide three interesting and specific facts...
"""

USER_QUESTION_TEMPLATE = """Context information is below.
---------------------
{context_str}
---------------------
Given the context, answer: {query_str}
"""
```

### Adjusting RAG Parameters

Fine-tune retrieval and chunking in `config.py`:

```python
CHUNK_SIZE = 512           # Size of text chunks
CHUNK_OVERLAP = 50         # Overlap between chunks
SIMILARITY_TOP_K = 3       # Number of chunks to retrieve
```

## 🧪 Development & Testing

### Run Tests

```bash
# Test Gemini integration
python test_gemini.py

# Test with mock data
python main.py --mock

# Test specific functionality
python -c "from modules.llm_interface import test_gemini_connection; test_gemini_connection()"
```

### Debugging

Enable detailed logging in your code:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or set in `config.py`:
```python
LOG_LEVEL = "DEBUG"  # Change from "INFO"
```

## 💰 Cost Estimation

### Gemini 2.5 Flash (Recommended)
- **Input:** $0.15 per 1M tokens (~$0.001 per profile)
- **Output:** $0.60 per 1M tokens
- **Embeddings:** FREE

**Example Monthly Costs:**
- 100 profiles/day: ~$3-5/month
- 500 profiles/day: ~$15-25/month
- 1,000 profiles/day: ~$30-50/month

### Gemini 2.5 Pro (Premium)
- **Input:** $1.25 per 1M tokens
- **Output:** $5.00 per 1M tokens
- **Embeddings:** FREE

About 8x more expensive than Flash, but highest quality.

## 🆚 Why Gemini vs IBM watsonx?

| Feature | Gemini | IBM watsonx |
|---------|--------|-------------|
| **Setup Complexity** | ✅ Simple (1 API key) | ⚠️ Complex (3 credentials) |
| **Free Tier** | ✅ Yes (1,500/day) | ❌ No |
| **Speed** | ⚡⚡⚡ Very Fast | ⚡⚡ Medium |
| **Context Window** | 1-2M tokens | 32K tokens |
| **Cost** | 💰 Lower | 💰💰 Higher |
| **Models Available** | 4+ options | 2 options |
| **Documentation** | ✅ Excellent | ⚠️ Limited |
| **API Simplicity** | ✅ REST API | ⚠️ Complex SDK |

## 🔒 Security & Privacy

- **API Keys**: Never commit `.env` file to version control
- **Data Storage**: Profile data is temporary and session-based
- **Logging**: Sensitive data is not logged by default
- **HTTPS**: All API calls use secure connections

**Best Practices:**
```bash
# Ensure .env is in .gitignore
echo ".env" >> .gitignore

# Use environment variables in production
export GEMINI_API_KEY="your-key-here"
```

## 🚀 Deployment

### Local Development
```bash
python app.py
# Access at http://localhost:5000
```

### Production Deployment

**Option 1: Heroku**
```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your_key
git push heroku main
```

**Option 2: Docker**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

**Option 3: Cloud Run (Google Cloud)**
- Easy integration with Gemini
- Automatic scaling
- Pay per use

## 🐛 Troubleshooting

### Common Issues

**Issue: "GEMINI_API_KEY not found"**
```bash
# Solution: Check your .env file
cat .env
# Ensure it contains: GEMINI_API_KEY=your_actual_key
```

**Issue: "Rate limit exceeded"**
```
Solution: Wait 60 seconds or upgrade to paid tier
Free tier: 15 requests/min, 1,500/day
```

**Issue: "Module not found: google.genai"**
```bash
# Solution: Install dependencies
pip install google-genai llama-index-llms-google-genai llama-index-embeddings-google-genai
```

**Issue: "Session expired" in chat**
```
Solution: Go back to Process tab and process the profile again
Sessions are temporary and lost when app restarts
```

**Issue: Slow responses**
```
Solution: 
1. Use gemini-2.5-flash instead of Pro
2. Reduce CHUNK_SIZE in config.py
3. Lower SIMILARITY_TOP_K value
```

## 📚 Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [LlamaIndex Documentation](https://docs.llamaindex.ai/)
- [ProxyCurl API](https://nubela.co/proxycurl)
- [Gradio Documentation](https://www.gradio.app/docs)
- [RAG Tutorial](https://docs.llamaindex.ai/en/stable/getting_started/starter_example/)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google** for providing the Gemini API and free tier
- **LlamaIndex** for the excellent RAG framework
- **ProxyCurl** for LinkedIn profile data extraction
- **Gradio** for the user-friendly web interface
- **Eden Marco** for the original tutorial inspiration

## 📊 Project Stats

- **Version:** 2.0 (Gemini Edition)
- **Python:** 3.9+
- **AI Model:** Google Gemini 2.5
- **Framework:** LlamaIndex 0.11.8
- **Interface:** Gradio 4.19.2

---

**Built with ❤️ using Google Gemini AI**

*Migrated from IBM watsonx to Gemini for better performance, lower costs, and simpler setup.*

## 🆕 Changelog

### v2.0.0 - Gemini Edition (December 2024)
- ✅ Migrated from IBM watsonx to Google Gemini
- ✅ Added support for Gemini 2.5 Flash and Pro models
- ✅ Simplified setup (1 API key instead of 3)
- ✅ Added free tier support (1,500 requests/day)
- ✅ Improved response speed (2-3x faster)
- ✅ Increased context window (1M tokens vs 32K)
- ✅ Enhanced error handling and logging
- ✅ Updated web interface with model selection
- ✅ Added comprehensive testing script

### v1.0.0 - Initial Release
- LinkedIn profile analysis with IBM watsonx
- RAG pipeline with vector search
- CLI and web interfaces
- Mock data support

---

**Questions?** Open an issue or reach out!

**Happy Networking! 🎉**