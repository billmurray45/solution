from sqlalchemy import String, func, DateTime, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import datetime
from app.core.enums import ModerationStatus


class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    name_surname: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, nullable=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    moderation_status: Mapped[ModerationStatus] = mapped_column(
        Enum(ModerationStatus, name="moderation_status_enum"),
        nullable=False,
        default=ModerationStatus.OPEN,
        server_default=ModerationStatus.OPEN.value
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
            f"status={self.moderation_status} answered={bool(self.admin_response)}>"
        )
