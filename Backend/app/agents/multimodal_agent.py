# app/agents/multimodal_agent.py
from langchain_core.messages import HumanMessage
from io import BytesIO
from typing import Optional, Any

from .llm_clients import gemini_model

async def process_multimodal_request(text_input: str, image_bytes: Optional[bytes]) -> str:
    """
    Calls the Gemini model with text and optional image data.
    
    Args:
        text_input: The user's text query.
        image_bytes: The raw byte data of the uploaded image, or None.
        
    Returns:
        The final text response from the Gemini model.
    """
    
    contents: list[Any] = [text_input]
    
    if image_bytes:
        # Construct the image part for the multimodal message
        image_part = {
            "image": BytesIO(image_bytes),
            "mime_type": "image/jpeg" # Assuming JPEG, but could be adjusted
        }
        contents.append(image_part)
        
    # Create the HumanMessage containing all parts
    message = HumanMessage(content=contents)
    
    # Invoke the model
    # .invoke() is synchronous, but running the endpoint async allows the server
    # to handle other requests while waiting for the LLM API response.
    response = gemini_model.invoke([message])
    
    return response.content