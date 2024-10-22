from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.operations.router import router as operations_router
from src.pages.router import pages_router as pages_router
from src.pages.router import home_router as home_router
from src.auth.router import auth_router, register_router, redirect_unauthorized_middleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.logging_config import setup_logging
import logging

setup_logging(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info('Launch App')

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(operations_router)
app.include_router(pages_router)
app.include_router(home_router)

app.include_router(auth_router)
app.include_router(register_router)

app.add_middleware(BaseHTTPMiddleware, dispatch=redirect_unauthorized_middleware)
