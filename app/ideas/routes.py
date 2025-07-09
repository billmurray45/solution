from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.dependencies.templates import templates
from app.ideas.crud import get_ideas, create_idea, delete_idea
from app.ideas.schemas import IdeaCreate
from app.ideas.models import Idea
from app.core.database import get_session
from typing import Optional

router = APIRouter()


@router.get("/ideas", response_class=HTMLResponse)
async def get_ideas_page(
    request: Request,
    page: int = 1,
    session: AsyncSession = Depends(get_session)
):
    page_size = 10
    ideas = await get_ideas(session, page=page, page_size=page_size)
    total_result = await session.execute(select(func.count()).select_from(Idea))
    total_count = total_result.scalar_one()
    total_pages = (total_count + page_size - 1) // page_size

    return templates.TemplateResponse(
        "ideas.html",
        {
            "request": request,
            "ideas": ideas,
            "current_page": page,
            "has_next": page < total_pages,
            "has_prev": page > 1,
            "total_pages": total_pages,
        }
    )


@router.post("/ideas")
async def post_idea(
    name_surname: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    subject: str = Form(...),
    message: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    idea_data = IdeaCreate(
        name_surname=name_surname,
        email=email,
        subject=subject,
        message=message,
    )
    await create_idea(session, idea_data)
    return RedirectResponse(url="/ideas", status_code=303)


@router.post("/ideas/{idea_id}/delete")
async def delete_idea_by_id(
    idea_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await delete_idea(idea_id, session)

    if not result:
        return {"message": "Идея не найдена или уже удалена."}

    return RedirectResponse(url="/ideas", status_code=303)
