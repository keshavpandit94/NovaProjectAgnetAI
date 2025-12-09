# app/schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """
    Schema for the auxiliary chat request data.
    """
    session_id: Optional[str] = None
    user_id: Optional[str] = None

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
        Configuration needed to map fields from the MongoDB/MongoEngine object.
        """
        from_attributes = True

class ChatResponse(BaseModel):
    """
    Schema for the successful response returned by the API endpoint.
    """
    session_id: str
    ai_response: str
    model_used: str 
    # NEW FIELD: Added to handle conditional history return in the router
    chat_history: List[HistoryItem] = Field(default_factory=list, 
                                            description="History only returned for logged-in users.")