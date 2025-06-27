from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.complaints.routers import router as complaints_router
from app.dependencies.templates import templates
from datetime import datetime
import uvicorn

app = FastAPI()
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
app.include_router(complaints_router)


@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "year": datetime.now().year})

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
