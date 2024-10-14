from httpx import AsyncClient
import logging

test_logger = logging.getLogger(__name__)

expense_operation_id = None


async def test_register_and_login(ac: AsyncClient):
    
    # Register user
    register_response = await ac.post("/auth/register", json={
        "email": "user0@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "user0"
    })

    # Authenticate user
    login_response = await ac.post("/auth/login", data={
        "username": "user0@example.com",
        "password": "string"
    })

    # Verify that the JWT token is set in cookies
    assert 'rent_keeper' in ac.cookies

    test_logger.debug(ac.cookies)

    # Reconfigure cookies, so that test client has access to protected routes
    ac.cookies = {'rent_keeper': ac.cookies['rent_keeper']}
    
    test_logger.debug(ac.cookies)
    
     
async def test_add_income_operation(ac: AsyncClient):
    
    response = await ac.post("/operations/income", json={
        "type_operation": "Income",
        "date_of_payment": "2024-09-10",
        "extra_info": "string",
        "gross_income": 80000,
        "comission": 10000,
        "revenue_after_comission": 70000,
        "date_in": "2024-09-06",
        "date_out": "2024-09-09",
        "fullname": "string",
        "phone": "string",
        "source": "Direct"
    })

    assert response.status_code == 200



async def test_add_expense_operation(ac: AsyncClient):
    global expense_operation_id

    response = await ac.post("/operations/expense", json={
        "type_operation": "Expense",
        "date_of_payment": "2024-09-30",
        "extra_info": "string",
        "total_expense": 20000
    })

    assert response.status_code == 200

    # Extract JSON from response
    response_json = response.json()
    
    test_logger.debug(response_json)
    
    # Check that response is as expected
    assert response_json['ok'] is True
    assert 'id' in response_json
    assert isinstance(response_json['id'], int)

    expense_operation_id = response_json['id']
    
    
async def test_edit_expense_operation(ac: AsyncClient):
    global expense_operation_id

    response = await ac.put(f"/operations/expense/{expense_operation_id}", json={
        "type_operation": "Expense",
        "date_of_payment": "2024-08-30",
        "extra_info": "string",
        "total_expense": 10000
    })

    # Extract JSON from response
    response_json = response.json()
    test_logger.debug(response_json)

    assert response.status_code == 200


async def test_delete_expense_operation(ac: AsyncClient):
    global expense_operation_id

    response = await ac.delete(f"/operations/delete/{expense_operation_id}")

    # Extract JSON from response
    response_json = response.json()
    test_logger.debug(response_json)

    assert response.status_code == 200