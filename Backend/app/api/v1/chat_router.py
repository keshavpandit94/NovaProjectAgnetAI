# app/api/v1/chat_router.py (UPDATED for Stateless Anonymous Search)
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional, List
from uuid import uuid4

# Import logic components
from app.agents.multimodal_agent import process_multimodal_request
from app.agents.image_handler import upload_image_to_cloudinary
from app.database.models import ConversationHistory
from app.schemas.chat import HistoryItem
from app.core.security import get_current_user_id 
# NOTE: We need the full user details, not just the ID, for some details. 
# We'll rely on the ID being present in the token payload.

router = APIRouter(prefix="/chat", tags=["AI Chat"])

# --- Helper Function for History Retrieval (Only for Logged-in Users) ---

def retrieve_user_history(user_id: str) -> List[HistoryItem]:
    """Retrieves chat history ONLY for the given logged-in user."""
    # Retrieve up to the last 10 entries for the user, ordered by time
    # This logic remains the same: retrieve history ONLY if user_id is provided
    history_docs = ConversationHistory.objects(user_id=user_id).order_by('-timestamp').limit(10)
    
    # Convert MongoDB documents to Pydantic models
    return [HistoryItem.model_validate(doc.to_mongo()) for doc in history_docs]


@router.post("/")
async def chat_endpoint(
    user_input_text: str = Form(...),
    image_file: Optional[UploadFile] = File(None),
    current_user_id: Optional[str] = Depends(get_current_user_id),
):
    
    is_logged_in = current_user_id is not None
    image_url = None
    image_bytes = None

    # --- 1. Determine Identity & Session ---
    if is_logged_in:
        # LOGGED-IN USER: Use their persistent ID
        user_id_to_store = current_user_id
        current_session_id = str(current_user_id) 
        is_anonymous_flag = False
    else:
        # ANONYMOUS USER: No history lookup is required. Generate a throwaway session_id for storage only.
        user_id_to_store = None
        current_session_id = str(uuid4()) # Use a new UUID for every anonymous request
        is_anonymous_flag = True

    # --- 2. Image Processing & Cloudinary Upload ---
    if image_file and image_file.filename:
        try:
            image_url = await upload_image_to_cloudinary(image_file)
            await image_file.seek(0)
            image_bytes = await image_file.read() 
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    # --- 3. Call AI Logic (Stateless) ---
    # NOTE: The process_multimodal_request function MUST be stateless here.
    # It should not reference any external memory or history object.
    try:
        ai_response = await process_multimodal_request(user_input_text, image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI processing failed: An internal error occurred.")

    # --- 4. Store History (For ALL users, for auditing/future retrieval) ---
    ConversationHistory(
        session_id=current_session_id,
        user_id=user_id_to_store,           
        is_anonymous=is_anonymous_flag,     
        user_input_text=user_input_text,
        ai_response_text=ai_response,
        image_url=image_url,
        model_used="gemini-2.5-flash"
    ).save()

    # --- 5. Retrieve History (CONDITIONALLY) ---
    user_history = []
    if is_logged_in:
        # ONLY retrieve and return history for LOGGED-IN users.
        user_history = retrieve_user_history(current_user_id)

    # --- 6. Return Response ---
    return {
        "session_id": current_session_id, # Can be thrown away by anonymous user
        "ai_response": ai_response,
        "model_used": "gemini-2.5-flash",
        "chat_history": user_history # Empty list for anonymous users
    }