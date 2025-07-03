from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class IdeaBase(BaseModel):
    name_surname: Optional[str] = Field(default=None, description="Name and surname of the person")
    email: Optional[str] = Field(default=None, description="Email address of the person")
    subject: str = Field(..., min_length=3, max_length=100, description="Subject of the idea")
    message: str = Field(..., min_length=20, description="Description of the idea")


class IdeaCreate(IdeaBase):
    pass


class IdeaRead(IdeaBase):
    id: int
    admin_response: Optional[str]
    external_user_id: Optional[int]
    created_at: datetime
    response_created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
