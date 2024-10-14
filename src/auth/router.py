from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from src.auth.base_config import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate

auth_router = APIRouter()
auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend), 
    prefix="/auth", 
    tags=["auth"]
)


register_router = APIRouter()
register_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)


# Middleware for redirecting unauthorized users
async def redirect_unauthorized_middleware(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 401:
        return RedirectResponse(url="/pages/login")
    return response
