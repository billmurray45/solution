from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.complaints.models import Complaint
from app.complaints.schemas import ComplaintCreate


async def create_complaint(session: AsyncSession, complaint_data: ComplaintCreate) -> Complaint:
    new_complaint = Complaint(**complaint_data.model_dump())
    session.add(new_complaint)
    await session.commit()
    await session.refresh(new_complaint)
    return new_complaint


async def get_complaints(session: AsyncSession, page: int = 1, page_size: int = 10) -> list[Complaint]:
    offset = (page - 1) * page_size
    result = await session.execute(select(Complaint).offset(offset).limit(page_size))
    return list(result.scalars().all())


async def delete_complaint(complaint_id: int, session: AsyncSession) -> dict | None:
    result = await session.execute(select(Complaint).where(Complaint.id == complaint_id))
    complaint = result.scalars().first()
    if not complaint:
        return None
    await session.delete(complaint)
    await session.commit()
    return {"message": "Complaint successfully deleted!"}
