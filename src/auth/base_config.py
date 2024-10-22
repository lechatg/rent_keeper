from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from src.auth.manager import get_user_manager
from src.auth.models import User
from src.config import SECRET_AUTH_KEY

cookie_transport = CookieTransport(cookie_name="rent_keeper", cookie_max_age=3600, cookie_secure=True)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH_KEY, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="cookie-jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


# Create FastAPIUsers instance
fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user()