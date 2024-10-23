document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('login_form').addEventListener('submit', async function(event) {
        event.preventDefault();

        const loginData = new FormData();
        loginData.set('username', document.getElementById('username_field').value);
        loginData.set('password', document.getElementById('password_field').value);

        axios.post(
            '/auth/login',
            loginData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            },
        )
        .then((response) => {
            console.log('Login successful:', response.data);
            // Redirect user if Login successful
            window.location.href = '/pages/operation/all';
        })
        .catch((error) => {
            console.error('Login failed:', error.response.data);
            
            alert('Login failed: ' + error.response.data.detail);
        });
        
    });
});