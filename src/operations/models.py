from src.database import Base


from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime, timezone
from sqlalchemy import ForeignKey, String, TIMESTAMP


class OperationOrm(Base):
    __tablename__ = "operation"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    id: Mapped[int] = mapped_column(primary_key=True)
    type_operation: Mapped[str]
    gross_income: Mapped[int | None]
    comission: Mapped[int | None]
    revenue_after_comission: Mapped[int | None]
    total_expense: Mapped[int | None]
    extra_info: Mapped[str | None]
    date_in: Mapped[date | None]
    date_out: Mapped[date | None]
    date_of_payment: Mapped[date]
    fullname: Mapped[str | None] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(20))
    source: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))

    
