// Function to Update Password
function submitForm() {

    // Get Form Elements
    var form = document.querySelector("form");
    var old_password = document.getElementById('old_passwd').value
    var new_password = document.getElementById('new_passwd').value;
    var new_password2 = document.getElementById('new_passwd2').value;
    
    var isValid = true;

    // Validate Old Password
    if (old_password.includes(' ')) {
        isValid = false;
        document.getElementById('old_passwd_val').innerText =
            "Password should not have whitespaces"
    }
    else if (!old_password) {
        isValid = false;
        document.getElementById('old_passwd_val').innerText =
            "Old password is required"
    } else {
        document.getElementById('old_passwd_val').innerText = "";
    }

    // Validate New Password
    if (new_password.includes(' ')) {
        isValid = false;
        document.getElementById('new_passwd_val').innerText =
            "Password should not have whitespaces"
    } else if (new_password.length < 8) {
        isValid = false;
        document.getElementById('new_passwd_val').innerText =
            "Password should be at least 8 characters long"
    }
    else if (!new_password) {
        isValid = false;
        document.getElementById('new_passwd_val').innerText =
            "New password is required"
    } else {
        document.getElementById('new_passwd_val').innerText = "";
    }

    // Validate Re-typed New Password
    if (new_password2.includes(' ')) {
        isValid = false;
        document.getElementById('new_passwd2_val').innerText =
            "Password should not have whitespaces"
    }
    else if (!new_password2) {     
        isValid = false;
        document.getElementById('new_passwd2_val').innerText =
            "Please re-type your password"
    }
    else if (new_password != new_password2) {
        isValid = false;
        document.getElementById('new_passwd2_val').innerText =
            "Password does not match"
    } else {
        document.getElementById('new_passwd2_val').innerText = "";
    }

    // Submit form if valid
    if (isValid) {
        if (confirm("Confirm Update Password?")) {
          form.submit();
        }
    }
}