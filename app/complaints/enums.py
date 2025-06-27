import enum


class ModerationStatus(str, enum.Enum):
    OPEN = "open"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"
