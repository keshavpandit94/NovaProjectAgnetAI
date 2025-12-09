from mongoengine import connect, disconnect_all
from app.core.config import settings

def connect_db():
    """Establishes the MongoDB connection on application startup."""
    try:
        # Use the URI from the configuration
        connect(host=settings.MONGO_URI, alias="default")
        print("✅ Successfully connected to MongoDB.")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        # Optionally, raise the exception or handle failure gracefully

def close_db():
    """Closes all MongoDB connections on application shutdown."""
    disconnect_all()
    print("🔌 MongoDB connection closed.")