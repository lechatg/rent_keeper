from sqlalchemy.ext.asyncio import AsyncSession
from src.operations import schemas, models
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from logging import getLogger
logger = getLogger(__name__)


async def create_operation(
        session: AsyncSession,
        operation_data: schemas.IncomeInWithUser | schemas.ExpenseInWithUser
) -> int:
    try:
        operation_dict = operation_data.model_dump()
        operation_orm = models.OperationOrm(**operation_dict)
        session.add(operation_orm)
        await session.flush()
        operation_id, operation_type = operation_orm.id, operation_orm.type_operation
        await session.commit()

        logger.info('An object of type %s with ID=%s has been added, сhanges saved to the database.', operation_type.value, operation_id)
        return operation_id
    
    except SQLAlchemyError as e:
        await session.rollback()
        logger.exception('Error occurred: %s', e)
        raise e 


async def get_operations_by_year(
        year: int,
        session: AsyncSession,
        user_id: int
) -> list[schemas.IncomeOut | schemas.ExpenseOut]:
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    query = select(models.OperationOrm).where(
        models.OperationOrm.date_of_payment >= start_date,
        models.OperationOrm.date_of_payment <= end_date,
        models.OperationOrm.user_id == user_id
    )
    
    result = await session.execute(query)
    rows = result.scalars().all()

    # Validate with pydantic schemas and store into list
    rows_schemas = []
    for row in rows:
        if row.type_operation == 'Income':
            rows_schemas.append(schemas.IncomeOut.model_validate(row))
        elif row.type_operation == 'Expense':
            rows_schemas.append(schemas.ExpenseOut.model_validate(row))

    # Sort schemas by date
    sorted_rows_schemas = sorted(rows_schemas, key=lambda x: x.date_of_payment)

    return sorted_rows_schemas


async def delete_operation(session: AsyncSession, operation_id: int, user_id: int) -> bool:
    result = await session.execute(select(models.OperationOrm).where(
        models.OperationOrm.id == operation_id, 
        models.OperationOrm.user_id == user_id
        ))
    operation = result.scalar_one_or_none()
    if operation:
        await session.delete(operation)
        await session.commit()
        return True
    return False


async def get_operation_by_id(session: AsyncSession, operation_id: int, user_id: int) -> None | schemas.IncomeOut | schemas.ExpenseOut:
    result = await session.execute(select(models.OperationOrm).where(
        models.OperationOrm.id == operation_id,
        models.OperationOrm.user_id == user_id
        ))
    operation = result.scalar_one_or_none()
    if operation is None:
        return None
    if operation.type_operation == 'Income':
        operation_schema = schemas.IncomeOut.model_validate(operation)
    elif operation.type_operation == 'Expense':
        operation_schema = schemas.ExpenseOut.model_validate(operation)
    return operation_schema


async def update_operation(
        session: AsyncSession,
        operation_id: int,
        operation_data: schemas.IncomeInWithUser | schemas.ExpenseInWithUser
) -> int | None:
    
    stmt = update(models.OperationOrm).where(
        (models.OperationOrm.id == operation_id) & (models.OperationOrm.user_id == operation_data.user_id)
        ).values(**operation_data.model_dump())

    result = await session.execute(stmt)
    await session.commit()
    
    if result.rowcount == 1:
        logger.info('Object with type %s and ID=%s successfully updated, changes in the database have been saved.', operation_data.type_operation, operation_id)
        return operation_id
    else:
        return None
    