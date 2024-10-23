document.addEventListener('DOMContentLoaded', function() {
    const yearSelect = document.getElementById('yearSelect');

    yearSelect.addEventListener('change', function() {
        fetchOperationsForYear(yearSelect.value);
    });

    // Load the current year operations on page load
    fetchOperationsForYear(yearSelect.value);
});

async function fetchOperationsForYear(year) {
    try {
        const response = await fetch(`/operations/${year}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
    
        const data = await response.json();
        const tableBody = document.getElementById('operationsTableBody');
        tableBody.innerHTML = '';

        let totalRevenueAfterCommission = 0;
        let totalExpenses = 0;

        data.forEach(operation => {
            const row = document.createElement('tr');
            
            row.setAttribute('data-id', operation.id); // Add data-id attribute

            row.className = operation.type_operation === 'Income' ? 'income-row' : 'expense-row';

            const dateInOut = operation.type_operation === 'Income' ? `In: ${formatDate(operation.date_in)}<br>Out: ${formatDate(operation.date_out)}` : '';

            const revenueAfterCommission = operation.revenue_after_comission || 0;
            const totalExpense = operation.total_expense || 0;

            totalRevenueAfterCommission += Number(revenueAfterCommission);
            totalExpenses += Number(totalExpense);

            row.innerHTML = `
                <td>${dateInOut}</td>
                <td>${formatDate(operation.date_of_payment)}</td>
                <td>${formatCurrency(operation.gross_income) || ''}</td>

                <td>${formatCurrency(operation.revenue_after_comission) || ''}</td>
                <td>${formatCurrency(operation.total_expense) || ''}</td>
                <td>${operation.fullname || ''}</td>
                <td>${operation.extra_info || ''}</td>
                <td>
                    <div class="d-flex gap-2">
                        <button class="btn btn-light btn-sm" onclick="showDeleteModal(${operation.id})">Delete</button>
                        <button class="btn btn-light btn-sm" onclick="editRowData(${operation.id})">Edit</button>
                    </div>
                </td>
            `;

            tableBody.appendChild(row);
        });

        // Update the totals in the table footer
        document.getElementById('totalRevenueAfterCommission').textContent = formatCurrency(totalRevenueAfterCommission);
        document.getElementById('totalExpenses').textContent = formatCurrency(totalExpenses);
    } catch (error) {
        console.error('Error fetching operations:', error);
    }
}

// Function to format date to dd.mm.yyyy
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-indexed
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
}

// Function to format currency values
function formatCurrency(amount, currencySymbol = '₽') {
    if (amount === null || amount === undefined) return '';
    // Convert number to string with thousands separators
    return `${Number(amount).toLocaleString()} ${currencySymbol}`;
}

// DELETION BLOCK
let operationIdToDelete = null;

// Function to show the delete confirmation modal
function showDeleteModal(operationId) {
    operationIdToDelete = operationId;
    const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
    deleteModal.show();
}

// Event listener for delete buttons
document.getElementById('confirmDelete').addEventListener('click', async () => {
    if (operationIdToDelete !== null) {
        console.log(`Operation ID for deletion: ${operationIdToDelete}`);
        await deleteOperation(operationIdToDelete);
        operationIdToDelete = null;
        const deleteModalElement = document.getElementById('deleteModal');
        const deleteModal = bootstrap.Modal.getInstance(deleteModalElement);
        deleteModal.hide();
    }
});

// Send DELETE request to server
async function deleteOperation(operationId) {
    try {
        const response = await fetch(`/operations/delete/${operationId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            console.log(`Operation with ID=${operationIdToDelete} deleted successfully!`);
            document.querySelector(`tr[data-id='${operationId}']`).remove();
            alert("Operation deleted successfully!");
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail}`);
        }
    } catch (error) {
        alert("An error occurred while deleting the operation.");
    }
}

async function editRowData(operationId) {
    try {
        window.location.href = `/pages/operation/form?operation_id=${operationId}`;
    } catch (error) {
        console.error('Error redirecting to the edit form page:', error);
    }
}

// Download Excel
document.getElementById('download-btn').addEventListener('click', async () => {
    const yearSelect = document.getElementById('yearSelect');
    const year = yearSelect.value;
    try {
        const response = await fetch(`/operations/${year}/download`);;
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `operations_report_${year}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error:', error);
    }
});


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