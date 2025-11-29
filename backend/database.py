"""
Database module - Supabase client initialization
"""
from supabase import create_client, Client
from config import settings


class Database:
    """Supabase database client wrapper"""
    
    _client: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client instance"""
        if cls._client is None:
            if not settings.supabase_url or not settings.supabase_service_key:
                raise ValueError(
                    "Supabase credentials not configured. "
                    "Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env file"
                )
            cls._client = create_client(
                settings.supabase_url,
                settings.supabase_service_key
            )
        return cls._client


# Convenience function
def get_db() -> Client:
    """Get database client instance"""
    return Database.get_client()
