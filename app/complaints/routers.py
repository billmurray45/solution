from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.dependencies.templates import templates
from app.complaints.crud import get_complaints, create_complaint
from app.complaints.schemas import ComplaintCreate
from app.complaints.models import Complaint
from app.core.database import get_session
from typing import Optional

router = APIRouter()


@router.get("/complaints", response_class=HTMLResponse)
async def get_complaints_page(
    request: Request,
    page: int = 1,
    session: AsyncSession = Depends(get_session)
):
    page_size = 10
    complaints = await get_complaints(session, page=page, page_size=page_size)

    total_result = await session.execute(select(func.count()).select_from(Complaint))
    total_count = total_result.scalar_one()
    total_pages = (total_count + page_size - 1) // page_size

    return (templates.TemplateResponse("complaints.html", {
        "request": request,
        "complaints": complaints,
        "current_page": page,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "total_pages": total_pages,
    }))


@router.post("/complaints")
async def post_complaint(
    name_surname: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    message: str = Form(...),
    session: AsyncSession = Depends(get_session)
):
    complaint_data = ComplaintCreate(
        name_surname=name_surname,
        email=email,
        message=message,
    )
    await create_complaint(session, complaint_data)
    return RedirectResponse(url="/complaints", status_code=303)
