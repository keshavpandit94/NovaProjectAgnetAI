from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

# Import components from your project structure
from app.core.security import get_current_user_id 
from app.database.models import ConversationHistory
from app.schemas.chat import HistoryItem #

router = APIRouter(prefix="/history", tags=["Chat History"])

# --- Helper Function (Reused from chat_router logic) ---

def retrieve_user_history(user_id: str) -> List[HistoryItem]:
    """Retrieves chat history ONLY for the given logged-in user, ordered by timestamp."""
    
    # Retrieve up to the last 50 entries for the user, ordered by time (most recent first)
    history_docs = ConversationHistory.objects(user_id=user_id).order_by('-timestamp').limit(50)
    
    # Convert MongoDB documents to Pydantic models
    # This uses the HistoryItem schema defined in chat.py
    return [HistoryItem.model_validate(doc.to_mongo()) for doc in history_docs]


@router.get("/", response_model=List[HistoryItem])
async def get_all_chat_history(
    # Requires an active JWT token to pass the user ID
    user_id: str = Depends(get_current_user_id),
) -> List[HistoryItem]:
    """
    Retrieves the chronological chat history for the currently logged-in user.
    """
    
    # Ensure a user ID was successfully extracted from the token
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed. User ID not found in token."
        )

    try:
        # 1. Fetch history using the helper function
        user_history = retrieve_user_history(user_id)
        
        # 2. Return the list of Pydantic models
        return user_history
        
    except Exception as e:
        print(f"Database error fetching history for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve chat history from the database."
        )