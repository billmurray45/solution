from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.complaints.routers import router as complaints_router
from app.complaints.models import Complaint
from app.ideas.routers import router as ideas_router
from app.ideas.models import Idea
from app.dependencies.templates import templates
from app.core.database import get_session
from datetime import datetime
import uvicorn

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
app.include_router(complaints_router)
app.include_router(ideas_router)


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request, session: AsyncSession = Depends(get_session)):
    last_idea = await session.scalar(
        select(Idea).order_by(Idea.created_at.desc()).limit(1)
    )
    last_complaint = await session.scalar(
        select(Complaint).order_by(Complaint.created_at.desc()).limit(1)
    )
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "last_complaint": last_complaint,
            "last_idea": last_idea,
            "year": datetime.now().year}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
