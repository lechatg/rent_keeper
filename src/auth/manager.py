
from typing import Optional


from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from src.auth.models import User
from src.auth.utils import get_user_db

from sqlalchemy.exc import IntegrityError

from logging import getLogger
logger = getLogger(__name__)

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    user_db_model = User

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        logger.info('User with id=%s and email=%s has registered.', user.id, user.email)

    
    async def on_after_login(
        self,
        user: models.UP,
        request: Optional[Request] = None,
        response: Optional[Response] = None,
    ) -> None:
        """
        Perform logic after user login.

        *You should overload this method to add your own logic.*

        :param user: The user that is logging in
        :param request: Optional FastAPI request
        :param response: Optional response built by the transport.
        Defaults to None
        """
        logger.info('User with id=%s and email=%s logged in.', user.id, user.email)
        return  # pragma: no cover

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        try:
            created_user = await self.user_db.create(user_dict)
        
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e.orig):
                raise exceptions.UserAlreadyExists() 
            

        await self.on_after_register(created_user, request)

        return created_user
    
    async def get_by_email(self, user_email: str) -> models.UP:
        """
        Get a user by e-mail (or username).

        :param user_email: E-mail of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_email(user_email)

        if user is None:
            # Check if user entered username instead of email
            user = await self.user_db.get_by_username(user_email)
            if user is None:
                raise exceptions.UserNotExists()

        return user

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)