"""Gradio web interface for the Icebreaker Bot with Google Gemini."""

import os
import sys
import logging
import uuid
import gradio as gr

from modules.data_extraction import extract_linkedin_profile
from modules.data_processing import split_profile_data, create_vector_database, verify_embeddings
from modules.llm_interface import change_llm_model
from modules.query_engine import generate_initial_facts, answer_user_query
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Dictionary to store active conversations
active_indices = {}

def process_profile(linkedin_url, api_key, use_mock, selected_model):
    """Process a LinkedIn profile and generate initial facts.
    
    Args:
        linkedin_url: LinkedIn profile URL to process.
        api_key: ProxyCurl API key.
        use_mock: Whether to use mock data.
        selected_model: LLM model to use.
        
    Returns:
        Initial facts about the profile and a session ID for this conversation.
    """
    try:
        # Change LLM model if needed
        if selected_model != config.LLM_MODEL_ID:
            change_llm_model(selected_model)
            
        # Use a default URL for mock data if none provided
        if use_mock and not linkedin_url:
            linkedin_url = "https://www.linkedin.com/in/leonkatsnelson/"
            
        # Extract profile data
        profile_data = extract_linkedin_profile(
            linkedin_url,
            api_key if not use_mock else None,
            mock=use_mock
        )
        
        if not profile_data:
            return "Failed to retrieve profile data. Please check the URL or API key.", None
        
        # Split data into nodes
        nodes = split_profile_data(profile_data)
        
        if not nodes:
            return "Failed to process profile data into nodes.", None
        
        # Create vector database
        index = create_vector_database(nodes)
        
        if not index:
            return "Failed to create vector database.", None
        
        # Verify embeddings
        if not verify_embeddings(index):
            logger.warning("Some embeddings may be missing or invalid")
        
        # Generate initial facts
        facts = generate_initial_facts(index)
        
        # Generate a unique session ID
        session_id = str(uuid.uuid4())
        
        # Store the index for this session
        active_indices[session_id] = index
        
        # Return the facts and session ID
        return f"Profile processed successfully!\n\nHere are 3 interesting facts about this person:\n\n{facts}", session_id
    
    except Exception as e:
        logger.error(f"Error in process_profile: {e}")
        return f"Error: {str(e)}", None

def chat_with_profile(session_id, user_query, chat_history):
    """Chat with a processed LinkedIn profile.
    
    Args:
        session_id: Session ID for this conversation.
        user_query: User's question.
        chat_history: Chat history.
        
    Returns:
        Updated chat history and cleared input.
    """
    if not session_id:
        return chat_history + [[user_query, "No profile loaded. Please process a LinkedIn profile first."]], ""
    
    if session_id not in active_indices:
        return chat_history + [[user_query, "Session expired. Please process the LinkedIn profile again."]], ""
    
    if not user_query.strip():
        return chat_history, ""
    
    try:
        # Get the index for this session
        index = active_indices[session_id]
        
        # Answer the user's query
        response = answer_user_query(index, user_query)
        
        # Update chat history
        return chat_history + [[user_query, response.response]], ""
    
    except Exception as e:
        logger.error(f"Error in chat_with_profile: {e}")
        return chat_history + [[user_query, f"Error: {str(e)}"]], ""

def create_gradio_interface():
    """Create the Gradio interface for the Icebreaker Bot."""
    # Define available Gemini models
    available_models = [
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]
    
    with gr.Blocks(title="LinkedIn Icebreaker Bot") as demo:
        gr.Markdown(
            """
            # 🤝 LinkedIn Icebreaker Bot
            ### Powered by Google Gemini AI
            
            Generate personalized icebreakers and chat about LinkedIn profiles using advanced AI.
            """
        )
        
        # Hidden state for session ID
        session_id = gr.State(value=None)
        
        with gr.Tab("🔍 Process LinkedIn Profile"):
            gr.Markdown(
                """
                ### Step 1: Process a Profile
                Enter a LinkedIn profile URL or use mock data to get started.
                """
            )
            
            with gr.Row():
                with gr.Column():
                    linkedin_url = gr.Textbox(
                        label="LinkedIn Profile URL",
                        placeholder="https://www.linkedin.com/in/username/",
                        info="Paste the full LinkedIn profile URL here"
                    )
                    api_key = gr.Textbox(
                        label="ProxyCurl API Key (Optional - Leave empty for mock data)",
                        placeholder="Your ProxyCurl API Key",
                        type="password",
                        value=config.PROXYCURL_API_KEY or "",
                        info="Get your API key from https://nubela.co/proxycurl"
                    )
                    use_mock = gr.Checkbox(
                        label="Use Mock Data", 
                        value=True,
                        info="Enable to test without API key"
                    )
                    model_dropdown = gr.Dropdown(
                        choices=available_models,
                        label="Select Gemini Model",
                        value=config.LLM_MODEL_ID,
                        info="Choose the AI model (Flash recommended for speed and cost)"
                    )
                    
                    with gr.Accordion("ℹ️ Model Information", open=False):
                        gr.Markdown(
                            """
                            **Gemini 2.5 Flash** (Recommended)
                            - Fast responses, low cost
                            - Excellent quality for most use cases
                            - 1M token context window
                            
                            **Gemini 2.5 Pro** (Premium)
                            - Highest quality responses
                            - Best for complex analysis
                            - 2M token context window
                            - Higher cost
                            """
                        )
                    
                    process_btn = gr.Button("🚀 Process Profile", variant="primary")
                
                with gr.Column():
                    result_text = gr.Textbox(
                        label="Initial Facts", 
                        lines=12,
                        placeholder="Interesting facts about the profile will appear here..."
                    )
            
            process_btn.click(
                fn=process_profile,
                inputs=[linkedin_url, api_key, use_mock, model_dropdown],
                outputs=[result_text, session_id]
            )
        
        with gr.Tab("💬 Chat"):
            gr.Markdown(
                """
                ### Step 2: Chat with the Profile
                Ask questions about the processed LinkedIn profile.
                """
            )
            
            # Chatbot without placeholder (not supported in Gradio 4.19.2)
            chatbot = gr.Chatbot(
                height=500,
                label="Chat History"
            )
            
            with gr.Row():
                chat_input = gr.Textbox(
                    label="Ask a question about the profile",
                    placeholder="What is this person's current job title?",
                    scale=4
                )
                chat_btn = gr.Button("Send", scale=1, variant="primary")
            
            gr.Markdown(
                """
                **Example questions:**
                - What is this person's current role?
                - What are their key skills?
                - What companies have they worked at?
                - What's an interesting icebreaker I could use?
                - Suggest conversation topics based on their interests
                """
            )
            
            # Update chat function to clear input
            chat_btn.click(
                fn=chat_with_profile,
                inputs=[session_id, chat_input, chatbot],
                outputs=[chatbot, chat_input]
            )
            
            chat_input.submit(
                fn=chat_with_profile,
                inputs=[session_id, chat_input, chatbot],
                outputs=[chatbot, chat_input]
            )
        
        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
                # About LinkedIn Icebreaker Bot
                
                ## 🎯 What is this?
                This application uses Google's Gemini AI to analyze LinkedIn profiles and generate:
                - Personalized conversation starters
                - Interesting facts about professionals
                - Interactive Q&A about profiles
                
                ## 🛠️ Technology Stack
                - **AI Model:** Google Gemini (2.5 Flash or 2.5 Pro)
                - **RAG Framework:** LlamaIndex
                - **Embeddings:** Google Text Embedding 004
                - **Web Interface:** Gradio
                - **Data Source:** ProxyCurl API (or mock data)
                
                ## 🚀 How to Use
                1. **Process a Profile:** Go to the "Process" tab and enter a LinkedIn URL
                2. **Review Facts:** See automatically generated interesting facts
                3. **Start Chatting:** Switch to the "Chat" tab and ask questions
                
                ## 🔑 API Keys
                - **Gemini API Key:** Get free at [Google AI Studio](https://aistudio.google.com/app/apikey)
                - **ProxyCurl API Key:** Optional, get at [ProxyCurl](https://nubela.co/proxycurl)
                
                ## 💡 Tips
                - Start with mock data to test the system
                - Use Gemini 2.5 Flash for best speed/cost balance
                - Upgrade to Pro for highest quality analysis
                - Ask specific questions for better responses
                
                ## 📊 Free Tier Limits
                - 15 requests per minute
                - 1,500 requests per day
                - 1M tokens per minute
                
                ---
                
                **Built with ❤️ using Google Gemini AI**
                
                Version: 2.0 (Gemini Edition)
                """
            )
    
    return demo

if __name__ == "__main__":
    # Check if API key is configured
    if not config.GEMINI_API_KEY:
        print("\n" + "="*60)
        print("⚠️  WARNING: GEMINI_API_KEY not found!")
        print("="*60)
        print("\nPlease set your Gemini API key in the .env file:")
        print("1. Copy .env.example to .env")
        print("2. Add your API key from: https://aistudio.google.com/app/apikey")
        print("\nYou can still run the app, but it will fail when processing profiles.")
        print("="*60 + "\n")
    
    demo = create_gradio_interface()
    
    # Launch the Gradio interface
    print("\n" + "="*60)
    print("🚀 Starting LinkedIn Icebreaker Bot")
    print("="*60)
    print(f"\nUsing model: {config.LLM_MODEL_ID}")
    print("Server will start on http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    demo.launch(
        server_name="0.0.0.0",  
        server_port=5000,
        share=True  # Creates a public link - set to False for local only
    )