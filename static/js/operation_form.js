function updateDisplayFields(typeOperation) {
    document.getElementById('expense-fields').style.display = typeOperation === 'Expense' ? 'block' : 'none';
    document.getElementById('income-fields').style.display = typeOperation === 'Income' ? 'block' : 'none';
    updateRequiredFields(typeOperation);
}

// Show different fields depending on type_operation
document.getElementById('type_operation').addEventListener('change', function() {
    const typeOperation = this.value;
    updateDisplayFields(typeOperation);
});

// Autofill revenue_after_comission based on gross_income and comission
document.getElementById('gross_income').addEventListener('input', calculateRevenue);
document.getElementById('comission').addEventListener('input', calculateRevenue);

function calculateRevenue() {
    const grossIncome = parseFloat(document.getElementById('gross_income').value) || 0;
    const comission = parseFloat(document.getElementById('comission').value) || 0;
    const revenueAfterComission = grossIncome - comission;
    document.getElementById('revenue_after_comission').value = revenueAfterComission;
}

// Update what fields are required based on type_operation
function updateRequiredFields(typeOperation) {
    const expenseFields = document.querySelectorAll('#expense-fields input');
    const incomeFields = document.querySelectorAll('#income-fields input, #income-fields select');

    if (typeOperation === 'Expense') {
        expenseFields.forEach(field => {
            field.addEventListener('input', updateValidationStyles);
            field.addEventListener('change', updateValidationStyles);
        });
        incomeFields.forEach(field => {
            field.removeEventListener('input', updateValidationStyles);
            field.removeEventListener('change', updateValidationStyles);
        });
    } else if (typeOperation === 'Income') {
        expenseFields.forEach(field => {
            field.removeEventListener('input', updateValidationStyles);
            field.removeEventListener('change', updateValidationStyles);
        });
        incomeFields.forEach(field => {
            field.addEventListener('input', updateValidationStyles);
            field.addEventListener('change', updateValidationStyles);
        });
    } else {
        expenseFields.forEach(field => {
            field.removeEventListener('input', updateValidationStyles);
            field.removeEventListener('change', updateValidationStyles);
        });
        incomeFields.forEach(field => {
            field.removeEventListener('input', updateValidationStyles);
            field.removeEventListener('change', updateValidationStyles);
        });
    }

    updateValidationStyles();
}

// Update styles for required fields
function updateValidationStyles() {
    const fields = document.querySelectorAll('input, select');
    fields.forEach(field => {
        const label = document.querySelector(`label[for="${field.id}"]`);
        const isRequired = label && label.querySelector('.required');
        
        if (isRequired) {
            if (field.value.trim() === '') {
                field.classList.add('invalid-field');
                field.classList.remove('valid-field');
            } else {
                field.classList.remove('invalid-field');
                field.classList.add('valid-field');
            }
        } else {
            field.classList.remove('invalid-field');
            field.classList.remove('valid-field');
        }
    });
}


document.addEventListener('DOMContentLoaded', function() {
    // DYNAMIC STYLES LOGIC
    // Update what fields are required based on selected type
    const typeOperation = document.getElementById('type_operation').value;
    updateRequiredFields(typeOperation);
    updateValidationStyles();

    // Add event listeners to all required fields to change styles upon input or change
    const fields = document.querySelectorAll('input, select');
    fields.forEach(field => {
        field.addEventListener('input', updateValidationStyles);
        field.addEventListener('change', updateValidationStyles);
    });

    // AUTOFILL FROM WITH DATA IF USER CAME TO EDIT
    const urlParams = new URLSearchParams(window.location.search);
    const operationId = urlParams.get('operation_id');

    if (operationId) {
        // Update the button text based on the presence of operation_id
        const submitButton = document.getElementById('submit-button');
        submitButton.textContent = 'Update Data';
        // Fetch data by operationId and then populate form with it
        fetchOperationData(operationId);
    }

});

// Collect data from fields into JSON and make PUT/POST request to update/add data to db
document.getElementById('operation-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    const typeOperation = data.type_operation.toLowerCase();
    // const url = typeOperation === 'expense' ? '/operations/expense' : '/operations/income';
    
    const urlParams = new URLSearchParams(window.location.search);
    const operationId = urlParams.get('operation_id');
    if (operationId) {
        console.log(`Update Operation with ID: ${operationId}`);
    }
    const url = operationId ? `/operations/${typeOperation}/${operationId}` : `/operations/${typeOperation}`;

    
    try {
        const response = await fetch(url, {
            method: operationId ? 'PUT' : 'POST',
            // method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log(result);

        document.getElementById('feedback-success').classList.remove('alert-blink');
        document.getElementById('feedback-error').classList.remove('alert-blink');


        if (response.ok) {
            document.getElementById('feedback-success').classList.add('d-none');
            document.getElementById('feedback-success').classList.remove('d-none');
            document.getElementById('feedback-error').classList.add('d-none');

            document.getElementById('feedback-success').classList.remove('alert-blink');
            void document.getElementById('feedback-success').offsetWidth; // Trigger reflow
            document.getElementById('feedback-success').classList.add('alert-blink');
            
        } else {
            const errorDetail = result.detail || 'Unknown error.';
            document.getElementById('feedback-error').textContent = `❌ Failed to add data. Error: ${errorDetail}`;
            document.getElementById('feedback-success').classList.add('d-none');
            document.getElementById('feedback-error').classList.remove('d-none');
            
            document.getElementById('feedback-error').classList.remove('alert-blink');
            void document.getElementById('feedback-error').offsetWidth; // Trigger reflow
            document.getElementById('feedback-error').classList.add('alert-blink');
            
        }

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('feedback-error').textContent = `❌ Request failed: ${error.message}`;
        document.getElementById('feedback-success').style.display = 'none';
        document.getElementById('feedback-error').style.display = 'block';
    }
});

// Fetch data for operation if user came with operationId
async function fetchOperationData(operationId) {
    try {
        const response = await fetch(`/operations/operation/${operationId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            populateForm(data);
        } else {
            throw new Error('Network response was not ok');
        }
    } catch (error) {
        console.error('Error fetching operation data:', error);
    }
}

// Populate form fields with data from server
function populateForm(data) {
    const form = document.getElementById('operation-form');
    for (const key in data) {
        if (data.hasOwnProperty(key)) {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                field.value = data[key];
            }
        }
    }

    // Check if type_operation field is populated and update the display of fields accordingly
    if (data.type_operation) {
        updateDisplayFields(data.type_operation);
    }
}

// Logout button
document.getElementById('logout-button').addEventListener('click', async function(event) {
    event.preventDefault();

    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            credentials: 'include' // Important for work with cookie
        });

        if (response.ok) {
            console.log('Logout successful');
            window.location.href = '/pages/login';
        } else {
            const errorData = await response.json();
            console.error('Logout failed:', errorData);
            alert('Logout failed: ' + errorData.detail);
        }
    } catch (error) {
        console.error('Logout failed:', error);
        alert('Logout failed: ' + error.message);
    }
});