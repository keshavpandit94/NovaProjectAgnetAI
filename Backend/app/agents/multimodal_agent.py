from google import genai
from google.genai.types import Part
from io import BytesIO
from typing import Optional, List, Union, Any

# NOTE: You will need to replace this import with your actual config and error handling
# from app.core.config import settings 

# --- 1. Client Initialization ---
# Initialize the client. In a production app, use proper setup via config.
# Assumes GEMINI_API_KEY is set in the environment or passed during client initialization.
try:
    # Use a placeholder client creation, replace with your actual setup
    client = genai.Client()
except Exception as e:
    # Handle the case where the API key is missing or the client fails to initialize
    print(f"Error initializing GenAI Client: {e}")
    client = None 

# --- 2. Helper Function to Create Image Part ---

def get_image_part_from_bytes(image_bytes: bytes, mime_type: str) -> Part:
    """Creates a Part object from raw image bytes for the API request."""
    # The GenAI SDK uses Part.from_bytes to handle binary data
    return Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type
    )

# --- 3. Main Multimodal Processing Function ---

async def process_multimodal_request(
    text_input: str, 
    image_bytes: Optional[bytes], 
    mime_type: str = "image/jpeg" # Default MIME type
) -> str:
    """
    Calls the Gemini model with text and optional image data using Google GenAI SDK.
    
    Args:
        text_input: The user's text query (can be an empty string if only image is provided).
        image_bytes: The raw byte data of the uploaded image, or None.
        mime_type: The MIME type of the image (e.g., 'image/png', 'image/avif').
        
    Returns:
        The final text response from the Gemini model.
    """
    if not client:
        return "Model client is not initialized. Check your API key and configuration."

    # The list of parts to send to the model
    contents: List[Union[str, Part]] = []
    
    # 1. Handle Image Upload
    prompt_text = text_input.strip()
    
    if image_bytes:
        # Create the image part and append it first
        image_part = get_image_part_from_bytes(image_bytes, mime_type)
        contents.append(image_part)
        
        # If image is present but text is empty, inject the detailed description prompt
        if not prompt_text:
            prompt_text = "What is in this image? Provide a full, detailed description including colors, location, and the natural setting."
            
    # 2. Handle Text Input and Default Behavior
    if not image_bytes and not prompt_text:
        # Case: Neither image nor text provided.
        return "Error: Please provide a text query, an image, or both."
        
    # Append the final determined text prompt
    contents.append(prompt_text)

    # 3. Invoke the model
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Using the same model specified in your history model
            contents=contents,
        )
        return response.text
    except Exception as e:
        # This will be caught by the router and converted to a 500 error
        raise RuntimeError(f"Model invocation failed: {e}")