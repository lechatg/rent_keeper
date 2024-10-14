from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from src.operations import schemas
from src.operations import crud
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

import pandas as pd
import io
from openpyxl.styles import Font

from sqlalchemy.exc import SQLAlchemyError

from src.auth.base_config import current_user
from src.auth.models import User

from logging import getLogger
logger = getLogger(__name__)

router = APIRouter(
    prefix='/operations',
    tags=['Rent Income & Expenses'],
    
    # Explicit router protection
    dependencies=[Depends(current_user)]
)


@router.post('/income', response_model=schemas.OperationCreated)
async def add_income_operation(
    operation_data: schemas.IncomeIn, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):  
    operation_data_with_user = schemas.IncomeInWithUser(**operation_data.model_dump(), user_id=user.id)
    try:
        operation_id = await crud.create_operation(session, operation_data_with_user)
        return {'ok': True, 'id': operation_id}
    except SQLAlchemyError as e:
        logger.exception("An error occurred while adding the item to the database.")
        raise HTTPException(status_code=500, detail="An error occurred while adding the item to the database.")


@router.put('/income/{operation_id}', response_model=schemas.OperationUpdated)
async def update_income_operation(
    operation_id: int,
    operation_data: schemas.IncomeIn, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    operation_data_with_user = schemas.IncomeInWithUser(**operation_data.model_dump(), user_id=user.id)

    updated_operation_id = await crud.update_operation(session, operation_id, operation_data_with_user)

    if updated_operation_id is None:
        logger.error("Failed to update Operation with ID=%s", operation_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to update Operation with ID={operation_id}"
        )
    return {'ok': True, 'updated': True, 'id': updated_operation_id}


@router.post('/expense', response_model=schemas.OperationCreated)
async def add_expense_operation(
    operation_data: schemas.ExpenseIn, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):  
    operation_data_with_user = schemas.ExpenseInWithUser(**operation_data.model_dump(), user_id=user.id)
    try:
        operation_id = await crud.create_operation(session, operation_data_with_user)
        return {'ok': True, 'id': operation_id}
    except SQLAlchemyError as e:
        logger.exception("An error occurred while adding the item to the database.")
        raise HTTPException(status_code=500, detail="An error occurred while adding the item to the database.")


@router.put('/expense/{operation_id}', response_model=schemas.OperationUpdated)
async def update_expense_operation(
    operation_id: int,
    operation_data: schemas.ExpenseIn, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    operation_data_with_user = schemas.ExpenseInWithUser(**operation_data.model_dump(), user_id=user.id)

    updated_operation_id = await crud.update_operation(session, operation_id, operation_data_with_user)

    if updated_operation_id is None:
        logger.error("Failed to update Operation with ID=%s", operation_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to update Operation with ID={operation_id}"
        )
    
    return {'ok': True, 'updated': True, 'id': updated_operation_id}


@router.get('/{year}', response_model=list[schemas.IncomeOut | schemas.ExpenseOut])
async def get_operations(
    year: int, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    rows_schemas = await crud.get_operations_by_year(year, session, user.id)
    return rows_schemas


@router.delete("/delete/{operation_id}", response_model=schemas.OperationDeleted, status_code=status.HTTP_200_OK)
async def delete_operation_route(
    operation_id: int, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    success = await crud.delete_operation(session, operation_id, user.id)
    if not success:
        logger.error("Failed to delete Operation with ID=%s: Operation not found", operation_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Operation not found")
    return schemas.OperationDeleted(ok=True, id=operation_id)


@router.get("/operation/{operation_id}", response_model=schemas.IncomeOut | schemas.ExpenseOut)
async def get_operation(
    operation_id: int, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    operation = await crud.get_operation_by_id(session, operation_id, user.id)
    if operation is None:
        logger.error("Operation with ID=%s not found.", operation_id)
        raise HTTPException(status_code=404, detail=f"Operation with ID={operation_id} not found")
    return operation


@router.get('/{year}/download')
async def download_excel(
    year: int, 
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    
    # Get data in pydantic schemas list
    data_rows_schemas = await get_operations(year, session, user)
    
    # Convert pydantic schemas into python dicts list
    data_dicts = []
    for row in data_rows_schemas:
        row_dict = row.model_dump()
        # Process Enum values ​​into strings
        for key, value in row_dict.items():
            if isinstance(value, Enum):
                row_dict[key] = value.value
        data_dicts.append(row_dict)

    df = pd.DataFrame(data_dicts)
    
    # Create in-memory excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=f'operations_{year}')
        
        # Customizing the Excel file
        worksheet = writer.sheets[f'operations_{year}']

        # Apply font to all cells
        for row in worksheet.iter_rows():
            for cell in row:
                cell.font = Font(size=14)
        
        # Apply bold font to header row
        for cell in worksheet[1]:  # Assuming the first row contains headers
            cell.font = Font(size=14, bold=True)

    output.seek(0)

    # Return file for download
    return StreamingResponse(output, 
                             media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                             headers={"Content-Disposition": "attachment; filename=report.xlsx"})