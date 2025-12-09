# app/agents/llm_clients.py
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

# Initialize the Gemini Model (using 2.5 Flash for speed and multimodal)
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.5,
    google_api_key=settings.GEMINI_API_KEY
)

# You can initialize other Gemini models here if needed, 
# but we will use the one above for the multimodal agent.