from motor.motor_asyncio import AsyncIOMotorClient
from .config import get_settings

settings = get_settings()

class Database:
    """Database connection manager for MongoDB."""
    
    client: AsyncIOMotorClient = None
    database = None
    
    @classmethod
    async def connect_db(cls):
        """Connect to MongoDB database."""
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_uri)
            cls.database = cls.client[settings.mongodb_db_name]
            print(f"Connected to MongoDB database: {settings.mongodb_db_name}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            print("MongoDB connection closed")
    
    @classmethod
    def get_db(cls):
        """Get database instance."""
        return cls.database
    
    @classmethod
    def get_collection(cls, collection_name: str):
        """Get a specific collection from the database."""
        return cls.database[collection_name]

# Database instance
db = Database()
