from sqlalchemy import String, func, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
from app.complaints.enums import ModerationStatus


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name_surname: Mapped[str] = mapped_column(String, nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    moderated: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus, name="moderation_status_enum"),
        nullable=False,
        default=ModerationStatus.OPEN
    )
    admin_response: Mapped[str] = mapped_column(Text, nullable=True)
    external_user_id: Mapped[int] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    response_created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
    )

    def __repr__(self):
        return (
            f"<Complaint id={self.id} external_user_id={self.external_user_id} "
            f"status={self.moderated} answered={bool(self.admin_response)}>"
        )
