document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('register_form').addEventListener('submit', async function(event) {
        event.preventDefault();

        // Collect data from form
        const email = document.getElementById('email_field').value;
        const username = document.getElementById('username_field').value;
        const password = document.getElementById('password_field').value;
        const repeatPassword = document.getElementById('repeat_password_field').value;

        const errorMessage = document.getElementById('passwords_dismatch_error_message');


        if (password !== repeatPassword) {
            errorMessage.textContent = 'Passwords do not match.';
        } else {
            errorMessage.textContent = '';
            
            const registerData = {
                email: email,
                username: username,
                password: password
            };


            try {
                // Submit the form using fetch method
                const response = await fetch('/auth/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(registerData)
                });
                

                // Handle response
                if (response.ok) {
                    const result = await response.json();
                    console.log('Registration successful:', result);
                    // Redirect to login page if Registration successful
                    window.location.href = '/pages/login';
                } else {
                    const result = await response.json()
                    console.error('Registration failed:', response.status, response.statusText, 'detail:', result.detail);
                    if (result.detail === "REGISTER_USER_ALREADY_EXISTS") {
                        console.log("User already exists");
                        alert("Registration failed: \nUser with this email and/or username already exists!");
                    }
                    
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    });
});