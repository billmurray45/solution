from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.auth.security import create_access_token, get_current_user_optional
from app.auth.schemas import LoginForm
from app.auth.service import auth_user_serivce

router = APIRouter()


@router.post("/login")
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user_optional)
):
    if current_user:
        return RedirectResponse("/", status_code=303)

    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        raise HTTPException(status_code=400, detail="Только AJAX")

    login_form = LoginForm(username=username, password=password)
    try:
        await auth_user_serivce(session, login_form)
        access_token = create_access_token({"sub": login_form.username})
        response = JSONResponse({"redirect": "/profile"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            max_age=60 * 30,
            samesite="lax"
        )
        return response
    except HTTPException as exc:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


@router.get("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("access_token")
    return response
