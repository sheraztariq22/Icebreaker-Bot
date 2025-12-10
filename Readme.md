# LinkedIn Icebreaker Bot

An AI-powered assistant that generates personalized icebreakers and conversation starters based on LinkedIn profiles. Built with IBM watsonx.ai and LlamaIndex, it helps make professional introductions more personal and engaging.

## 🌟 Features

- **LinkedIn Profile Analysis**: Extract professional data using ProxyCurl API or use mock data
- **AI-Powered Insights**: Generate interesting facts about a person's career/education 
- **Personalized Q&A**: Answer specific questions about the person's background
- **Two Interfaces**: Command-line tool for quick usage and web UI for user-friendly interaction
- **Flexible**: Use mock data for practice or connect to real LinkedIn profiles

## 🚀 Quick Start

### Prerequisites

- Python 3.11+, < 3.13
- A ProxyCurl API key (optional - mock data available)

### Installation

1. Clone the repository:
```bash
git clone <Link of Repo>
cd Icebreaker-Bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
OR 
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Add your ProxyCurl API key to `config.py`:
```python
PROXYCURL_API_KEY = "your-api-key-here"
```

### Using the Command Line Interface

Run the bot using the terminal:

```bash
# Use mock data (no API key needed)
python main.py --mock

# OR use a real LinkedIn profile
python main.py --url "https://www.linkedin.com/in/username/" --api-key "your-api-key"
```

### Using the Web Interface

Launch the web app:

```bash
python app.py
```

Then open your browser to the URL shown in the terminal (typically http://127.0.0.1:7860).

## 🧠 How It Works

The Icebreaker Bot uses a Retrieval-Augmented Generation (RAG) pipeline:

1. **Data Extraction**: LinkedIn profile data is retrieved via ProxyCurl API or mock data
2. **Text Processing**: Profile data is split into manageable chunks
3. **Vector Embedding**: Text chunks are converted to vector embeddings using IBM watsonx
4. **Storage**: Embeddings are stored in a vector database
5. **Query & Generation**: When asked a question, relevant profile sections are retrieved and an IBM watsonx LLM generates contextually accurate responses

## 🛠️ Project Structure

```
icebreaker_bot/
├── requirements.txt           # Dependencies
├── config.py                  # Configuration settings
├── modules/
│   ├── __init__.py
│   ├── data_extraction.py     # LinkedIn profile data extraction
│   ├── data_processing.py     # Data splitting and indexing
│   ├── llm_interface.py       # LLM setup and interaction
│   └── query_engine.py        # Query processing and response generation
├── app.py                     # Gradio web interface
└── main.py                    # CLI application
```

## 📝 Examples

Here are some example questions you can ask:

- "What is this person's current job title?"
- "Where did they get their education?"
- "What skills do they have related to machine learning?"
- "How long have they been working at their current company?"
- "What was their career progression?"

## 🧪 Customization

### Using Different LLM Models

You can switch between available models:

```bash
python main.py --mock --model "meta-llama/llama-3-3-70b-instruct"
```

Or in the web interface, select from the dropdown menu.

### Adjusting Response Style

Edit the prompt templates in `config.py` to change how responses are generated:

```python
INITIAL_FACTS_TEMPLATE = """
You are an AI assistant that provides detailed answers based on the provided context.
...
"""
```

## 👩‍💻 Development


# Test the entire pipeline
python main.py --mock --test
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- IBM watsonx.ai for providing the LLM and embedding models
- LlamaIndex for the data indexing and retrieval framework
- ProxyCurl for LinkedIn profile data extraction
- Eden Marco for the original tutorial inspiration
