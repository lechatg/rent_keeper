from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from src.auth.base_config import current_user
from src.auth.models import User

router = APIRouter(
    prefix='/pages',
    tags=['Pages'],
)

templates = Jinja2Templates(directory="templates")


@router.get("/operation/form")
async def get_new_form_page(request: Request, operation_id: int | None = None, user: User = Depends(current_user)):
    return templates.TemplateResponse("operation_form.html", {"request": request, "operation_id": operation_id, "username": user.username, "user_id": user.id})


@router.get("/operation/all")
async def get_operations_page(request: Request, user: User = Depends(current_user)):
    current_year = datetime.now().year
    return templates.TemplateResponse("operations.html", {
        "request": request,
        "current_year": current_year,
        "username": user.username,
        "user_id": user.id
    })


@router.get("/login")
async def get_new_form_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, })


@router.get("/register")
async def get_new_form_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, })