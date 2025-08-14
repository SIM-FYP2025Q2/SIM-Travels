// Search User Accounts
function searchUserAccounts() {
    // Get Search Input
    var searchTermInput = document.getElementById("search_term");
    var searchTerm = searchTermInput.value;

    // Alphanumeric & Single Whitespace Regex
    searchTerm = searchTerm.replace(/[^a-zA-Z0-9\s]+/g, '');
    searchTerm = searchTerm.replace(/\s+/g, ' ');

    // Update URL to include GET['q'] Parameter
    window.location.href = 'admin.php?q="' + searchTerm + '"';
}

// Function to View User
function viewUser(id) {
    // Fetch User details from the server
    fetch(`../controllers/ViewUserAccountController.php?id=${id}`)
    .then(response => response.json())
    .then(data => {
        // Populate modal with data
        document.getElementById('r_username').value = data.username;
        document.getElementById('r_email').value = data.email;
        document.getElementById('r_is_admin').value = data.is_admin == 1 ? 'Yes' : 'No';
        document.getElementById('r_is_active').value = data.is_active == 1 ? 'Yes' : 'No';
    })
    .catch(error => {
        console.error("Error fetching user data:", error);
        alert("Unable to retrieve user details. Please try again later.");
    });
}

// Function to Update User
function updateUser(id) {
    // Fetch User details from the server
    fetch(`../controllers/ViewUserAccountController.php?id=${id}`)
    .then(response => response.json())
    .then(data => {
        // Populate modal with data
        document.getElementById('userId').value = data.id;
        document.getElementById('u_username').value = data.username;
        document.getElementById('u_email').value = data.email;
        document.getElementById('u_is_admin').value = data.is_admin;
        document.getElementById('u_is_active').value = data.is_active;
        document.getElementById('u_password').value = ''; // Clear password field
    })
    .catch(error => {
        console.error("Error fetching user data:", error);
        alert("Unable to retrieve user details. Please try again later.");
    });
}

// Function to Update User Account
async function updateUserForm() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('updateUserModal'));

    // Get Form Data
    var userId = document.getElementById('userId').value;
    var username = document.getElementById('u_username').value.trim();
    var email = document.getElementById('u_email').value.trim();
    var isAdmin = document.getElementById('u_is_admin').value;
    var isActive = document.getElementById('u_is_active').value;
    var password = document.getElementById('u_password').value;

    // Validate Form Data
    if (username === '' || email === '') {
        alert('Please fill in all fields.');
        return;
    }

    // Username validation: no whitespaces
    if (username.includes(' ')) {
        alert('Username cannot contain whitespaces.');
        return;
    }

    // Email validation: basic format check
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (password !== '') {
        if (password.includes(' ')) {
            alert('Password cannot contain whitespaces.');
            return;
        }
        if (password.length < 8) {
            alert('Password must be at least 8 characters long.');
            return;
        }
    }

    // Prepare Form Data
    var data = new FormData();
    data.append('id', userId);
    data.append('username', username);
    data.append('email', email);
    data.append('is_admin', isAdmin);
    data.append('is_active', isActive);
    data.append('password', password);

    try {
        // Send POST Request
        const response = await fetch('../controllers/UpdateUserAccountController.php', {
            method: 'POST',
            body: data,
        });

        // Check Response Value
        const responseVal = await response.json();
        if (responseVal.isSuccess) {
            alert('User updated successfully!');
            modal.hide()
            window.location.reload(true);
        } else {
            alert('User update failed, please try again later.');
            modal.hide();
            window.location.reload(true);
        }
    } catch (error) {
        console.error("Error during user update:", error);
        alert('User update failed, please try again later.');
        modal.hide();
        window.location.reload(true);
    }
}

// Function to Delete User
async function deleteUser(id) {
    // Confirm Prompt
    if (confirm("Are you sure you want to delete this user?")) {
        try {
            // Prepare Form Data
            var data = new FormData();
            data.append('id', id);

            // Send DELETE Request
            const response = await fetch('../controllers/DeleteUserAccountController.php', {
                method: 'POST',
                body: data,
            });

            // Check Response Value
            const responseVal = await response.json();
            if (responseVal.isSuccess) {
                alert('User deleted successfully!');
                window.location.reload(true);
            } else {
                alert('User deletion failed, please try again later.');
                window.location.reload(true);
            }
        } catch (error) {
            console.error("Error during user deletion:", error);
            alert('Unknown error occurred during user deletion, please try again later.');
            window.location.reload(true);
        }
    }
}

// Function to Create User
async function createUser() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('createUserModal'));

    // Get Form Data
    var username = document.getElementById('c_username').value.trim();
    var email = document.getElementById('c_email').value.trim();
    var password = document.getElementById('c_password').value;

    // Validate Form Data
    if (username === '' || email === '' || password === '') {
        alert('Please fill in all fields.');
        return;
    }

    // Email validation: basic format check
    const emailRegex = /\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    if (password.includes(' ')) {
        alert('Password cannot contain whitespaces.');
        return;
    }
    if (password.length < 8) {
        alert('Password must be at least 8 characters long.');
        return;
    }

    // Prepare Form Data
    var data = new FormData();
    data.append('username', username);
    data.append('email', email);
    data.append('password', password);

    try {
        // Send POST Request
        const response = await fetch('../controllers/RegisterController.php', {
            method: 'POST',
            body: data,
        });

        // Check Response Value
        const responseVal = await response.json();
        if (responseVal.success) {
            alert(responseVal.message);
            modal.hide();
            window.location.reload(true);
        } else {
            alert(responseVal.message);
        }
    } catch (error) {
        console.error("Error during user creation:", error);
        alert('User creation failed, please try again later.');
    }
}