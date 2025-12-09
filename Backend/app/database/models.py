# app/database/models.py
from mongoengine import Document, StringField, DateTimeField, BooleanField, connect
from datetime import datetime

class User(Document):
    """Stores user account information for authentication."""
    email = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True) # NEW
    name = StringField() # NEW
    dob = DateTimeField() # NEW
    hashed_password = StringField(required=True)
    is_active = BooleanField(default=True)
    
    meta = {'collection': 'users'}

class ConversationHistory(Document):
    """Stores one turn of a user-AI interaction."""
    
    # User Identification
    session_id = StringField(required=True)
    # Stores the User ID (as a string) if logged in, otherwise None
    user_id = StringField() 
    is_anonymous = BooleanField(default=False)
    
    # Interaction Data
    user_input_text = StringField(required=True)
    ai_response_text = StringField(required=True)
    image_url = StringField() 
    
    # Model Metadata
    model_used = StringField(required=True, default="gemini-2.5-flash")
    timestamp = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'conversation_history'}