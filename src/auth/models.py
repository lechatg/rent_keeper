from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Integer, String, TIMESTAMP
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class User(SQLAlchemyBaseUserTable[int], Base):
    # __tablename__ already defined as "user" in SQLAlchemyBaseUserTable, duplicate here for clarity
    __tablename__ = "user"

    # Recommended approach for id in fastapi-users docs
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Custom fields
    username: Mapped[str] = mapped_column(String(length=20), unique=True, nullable=False)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))


    # Fields below - fields predefined in class SQLAlchemyBaseUserTable, duplicate here for clarity
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
