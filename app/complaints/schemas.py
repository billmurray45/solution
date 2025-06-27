from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.complaints.enums import ModerationStatus


class ComplaintBase(BaseModel):
    name_surname: Optional[str] = Field(default=None, description="Name and surname of the person")
    email: Optional[str] = Field(default=None, description="Email address of the person")
    message: str = Field(..., description="Description of the complaint")
    moderated: ModerationStatus = Field(default=ModerationStatus.OPEN, description="Moderation status")


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintRead(ComplaintBase):
    id: int
    admin_response: Optional[str]
    external_user_id: Optional[int]
    created_at: datetime
    response_created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
