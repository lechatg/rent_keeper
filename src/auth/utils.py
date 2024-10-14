from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import get_async_session

from sqlalchemy import select

    
class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase[User, int]):
    async def get_by_username(self, email: str) -> User | None:
        # Compare with email here, because there is single "email" field for both email and username
        statement = select(self.user_table).where(self.user_table.username == email)
        return await self._get_user(statement)
    

# DEFAULT get_user_db:
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)


# CUSTOM get_user_db:
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomSQLAlchemyUserDatabase(session, User)