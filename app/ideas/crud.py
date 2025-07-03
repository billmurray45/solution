from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ideas.models import Idea
from app.ideas.schemas import IdeaCreate


async def create_idea(session: AsyncSession, idea_data: IdeaCreate) -> Idea:
    new_idea = Idea(**idea_data.model_dump())
    session.add(new_idea)
    await session.commit()
    await session.refresh(new_idea)
    return new_idea


async def get_ideas(session: AsyncSession, page: int = 1, page_size: int = 10) -> list[Idea]:
    offset = (page - 1) * page_size
    result = await session.execute(select(Idea).offset(offset).limit(page_size))
    return list(result.scalars().all())


async def delete_idea(idea_id: int, session: AsyncSession) -> dict | None:
    result = await session.execute(select(Idea).where(Idea.id == idea_id))
    idea = result.scalars().first()
    if not idea:
        return None
    await session.delete(idea)
    await session.commit()
    return {"message": "Idea successfully deleted!"}
