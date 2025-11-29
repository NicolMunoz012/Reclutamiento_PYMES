"""
Storage Service - Upload files to Supabase Storage
"""
from database import get_db
from typing import Optional
import uuid


class StorageService:
    """Service for file storage operations"""
    
    def __init__(self):
        self.bucket_name = "convocatoria"
    
    async def upload_cv(
        self,
        file_bytes: bytes,
        candidato_id: str,
        filename: str
    ) -> Optional[str]:
        """
        Upload CV PDF to Supabase Storage
        
        Args:
            file_bytes: PDF file content
            candidato_id: Candidate ID
            filename: Original filename
            
        Returns:
            Public URL of uploaded file or None if failed
        """
        try:
            db = get_db()
            
            # Generate unique filename
            file_extension = filename.split('.')[-1] if '.' in filename else 'pdf'
            unique_filename = f"{candidato_id}_{uuid.uuid4()}.{file_extension}"
            
            # Upload to Supabase Storage
            response = db.storage.from_(self.bucket_name).upload(
                path=unique_filename,
                file=file_bytes,
                file_options={"content-type": "application/pdf"}
            )
            
            # Get public URL
            public_url = db.storage.from_(self.bucket_name).get_public_url(unique_filename)
            
            return public_url
            
        except Exception as e:
            print(f"Error uploading file to storage: {e}")
            return None


# Singleton instance
storage_service = StorageService()
