from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.routes import router as users_router
from app.auth.routes import router as auth_router
from app.complaints.routes import router as complaints_router
from app.ideas.routes import router as ideas_router
from app.auth.security import get_current_user_optional
from app.complaints.models import Complaint
from app.ideas.models import Idea
from app.dependencies.templates import templates
from app.core.database import get_session
from app.core.parser import router as parser_router, fetch_news
from datetime import datetime
import uvicorn

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
app.include_router(complaints_router)
app.include_router(ideas_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(parser_router)


@app.get("/", response_class=HTMLResponse)
async def get_home_page(
        request: Request,
        session: AsyncSession = Depends(get_session),
        current_user=Depends(get_current_user_optional)
):
    last_ideas = (await session.scalars(select(Idea).order_by(Idea.created_at.desc()).limit(3))).all()
    last_complaints = (await session.scalars(select(Complaint).order_by(Complaint.created_at.desc()).limit(3))).all()
    news = fetch_news()[:8]
    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "last_complaints": last_complaints,
            "last_ideas": last_ideas,
            "current_user": current_user,
            "news": news,
            "year": datetime.now().year
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
