from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

class Recipient(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    pdf_b64: str                        # PDF already in Base64
    vars: Optional[Dict] = None 