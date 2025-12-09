import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from app.core.config import settings
from typing import IO

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

async def upload_image_to_cloudinary(file: UploadFile) -> str:
    """
    Uploads the image file to Cloudinary and returns the secure URL.
    
    Args:
        file: The UploadFile object from the FastAPI request.
        
    Returns:
        The secure URL of the uploaded image.
    """
    
    # Read file content into memory stream (Cloudinary SDK expects a stream/path)
    # Note: For very large files, this should be chunked, but this works for typical uploads.
    file_content = await file.read()
    
    # Use cloudinary.uploader.upload_resource to upload the raw binary data
    upload_result = cloudinary.uploader.upload(
        file=file_content,
        folder="ai_agent_uploads", # Optional: Organize uploads in a folder
        resource_type="image"
    )
    
    # Return the secure URL provided by Cloudinary
    return upload_result.get("secure_url")