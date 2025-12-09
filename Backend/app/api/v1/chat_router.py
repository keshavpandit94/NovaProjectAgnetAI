# app/api/endpoints/chat_router.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from typing import Optional, List, Annotated
from uuid import uuid4
from datetime import datetime

# Import logic components (Adjust paths as needed for your project structure)
from app.agents.multimodal_agent import process_multimodal_request
from app.agents.image_handler import upload_image_to_cloudinary
from app.database.models import ConversationHistory
from app.schemas.chat import HistoryItem, ChatResponse 
from app.core.security import get_current_user_id 

router = APIRouter(prefix="/chat", tags=["AI Chat"])

# --- Helper Function for History Retrieval (Only for Logged-in Users) ---

def retrieve_user_history(user_id: str) -> List[HistoryItem]:
    """Retrieves chat history ONLY for the given logged-in user."""
    # Retrieve up to the last 10 entries for the user, ordered by time
    history_docs = ConversationHistory.objects(user_id=user_id).order_by('-timestamp').limit(10)
    
    # Convert MongoDB documents to Pydantic models (using model_validate for safety)
    return [HistoryItem.model_validate(doc.to_mongo()) for doc in history_docs]


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    # NOTE: user_input_text defaults to an empty string ("") if not provided in the form
    user_input_text: Annotated[str, Form()] = "", 
    
    # FIX APPLIED HERE: Default value (= None) is set outside the Annotated type.
    image_file: Annotated[Optional[UploadFile], File()] = None, 
    
    current_user_id: Optional[str] = Depends(get_current_user_id),
):
    
    # --- 1. Identity & Session Setup ---
    is_logged_in = current_user_id is not None
    
    if is_logged_in:
        user_id_to_store = current_user_id
        current_session_id = str(current_user_id)
        is_anonymous_flag = False
    else:
        user_id_to_store = None
        current_session_id = str(uuid4())
        is_anonymous_flag = True

    # --- 2. Initial Input Validation ---
    if not user_input_text.strip() and not image_file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either text input or an image file."
        )
        
    # --- 3. Image Processing & Cloudinary Upload ---
    image_bytes = None
    image_url_to_save: Optional[str] = None
    image_mime_type = "image/jpeg" 
    
    if image_file and image_file.filename:
        # Get MIME Type
        if image_file.content_type:
            image_mime_type = image_file.content_type
            
        try:
            # a. Read bytes for the LLM agent (Consumes the stream)
            image_bytes = await image_file.read() 
            
            # b. Reset stream for the Cloudinary uploader
            await image_file.seek(0) 
            
            # c. Upload to Cloudinary
            image_url_to_save = await upload_image_to_cloudinary(image_file)
            
        except Exception as e:
            print(f"Cloudinary upload/file read failed: {e}")
            image_bytes = None 
            if not user_input_text.strip():
                 raise HTTPException(status_code=500, detail="Image upload failed and no text was provided.")


    # --- 4. Call AI Logic ---
    try:
        ai_response = await process_multimodal_request(
            text_input=user_input_text, 
            image_bytes=image_bytes,
            mime_type=image_mime_type # Passed for best model performance
        )
    except RuntimeError as e: # Catch the specific exception raised in multimodal_agent.py
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"AI processing failed: {e}")
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred during AI processing.")


    # --- 5. Store History ---
    try:
        ConversationHistory(
            session_id=current_session_id,
            user_id=user_id_to_store,           
            is_anonymous=is_anonymous_flag,     
            user_input_text=user_input_text,
            ai_response_text=ai_response,
            image_url=image_url_to_save,
            model_used="gemini-2.5-flash",
            timestamp=datetime.utcnow()
        ).save()
    except Exception as e:
        print(f"Error saving conversation history: {e}")

    # --- 6. Retrieve History (CONDITIONALLY) ---
    user_history = []
    if is_logged_in:
        user_history = retrieve_user_history(current_user_id)

    # --- 7. Return Response ---
    return ChatResponse(
        session_id=current_session_id, 
        ai_response=ai_response,
        model_used="gemini-2.5-flash",
        chat_history=user_history
    )