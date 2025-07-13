from pydantic import BaseModel, Field
from typing import Optional

class JornalEntryCreate(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(..., max_length=200)
    content: str
    tags: Optional[List[str]] = []
