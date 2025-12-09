# app/schemas/chat.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    """
    Schema for the auxiliary chat request data.
    
    NOTE: The core inputs (user_input_text and image_file) are handled 
    directly as Form/File parameters in the router for multimodal input, 
    but these fields help track the session context.
    """
    session_id: Optional[str] = None  # Temporary ID for anonymous users
    user_id: Optional[str] = None     # User ID for logged-in users (passed via dependency/form)

class ChatResponse(BaseModel):
    """
    Schema for the successful response returned by the API endpoint.
    """
    session_id: str
    ai_response: str
    model_used: str 

class HistoryItem(BaseModel):
    """
    Schema for a single conversation entry as it might be retrieved 
    from the database (e.g., for a history endpoint).
    """
    session_id: str
    user_id: Optional[str] = None
    is_anonymous: bool
    user_input_text: str
    ai_response_text: str
    image_url: Optional[str] = None
    timestamp: datetime # Uses Python's datetime type

    class Config:
        """
        Configuration needed to map fields from the MongoDB/MongoEngine object
        when retrieving history (e.g., in a GET /history endpoint).
        """
        # This setting is for Pydantic V2 and ensures it can read data from 
        # arbitrary object types (like MongoEngine Document objects)
        from_attributes = True