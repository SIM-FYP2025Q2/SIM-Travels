<?php

session_start();

if (!isset($_SESSION['IS_LOGGED_IN'])) {
    // Redirecting to Login Page
    header("Location: ../login.php");
    exit();
}

// Check if the user is an admin
if ($_SESSION['is_admin'] == 1) {
    // Redirect to an admin page
    header("Location: admin.php"); // Redirect to the FAQ homepage
    exit();
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Update Password</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.css" rel="stylesheet">
  <link rel="stylesheet" href="../css/custom_bootstrap.css" />
</head>
<body>

  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg bg-light border-bottom shadow-sm px-5 py-2">
    <div class="container-fluid">
      <!-- Brand Logo -->
      <a class="navbar-brand" href="home.php">
        <img src="../img/icon-logo.png" alt="Logo" height="32">
      </a>
      <!-- Page Links -->
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="home.php">Knowledge Base</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="categories.php">Categories</a>
          </li>
        </ul>
      </div>

      <!-- User Dropdown Menu -->
      <div class="d-flex align-items-center gap-3">
        <div class="dropdown">
            <button
              class="btn btn-primary d-flex align-items-center gap-2 dropdown-toggle"
              type="button"
              data-bs-toggle="dropdown"
              aria-expanded="false">
                <ion-icon name="person-circle-outline" style="font-size: 1.2rem;"></ion-icon>
                <?php echo $_SESSION['username']; ?>
            </button>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="../logout.php">Logout</a></li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <!-- Create Form -->
  <div class="container mt-4">
    <h2>Update Password</h3>
    <hr/>
  </div>
  <div class="container-md card p-4 shadow-lg">
    <?php
      if (isset($_GET['status'])) {
        if ($_GET['status'] == '1') {
          echo '<div class="alert alert-success" role="alert">';
          echo 'Successfully updated password!';
          echo '</div>';
        } else if ($_GET['status'] == '0'){
          echo '<div class="alert alert-danger" role="alert">';
          echo 'Failed to update password, incorrect old password.';
          echo '</div>';
        } else {
          echo '<div class="alert alert-danger" role="alert">';
          echo 'Failed to update password, an error has occured.';
          echo '</div>'; 
        }
      }
    ?>
    <form id="updatePasswordForm" action="../controllers/UpdatePasswordController.php" method="POST">
      
      <div class="mb-3">
        <input type="hidden" id="userID" name="userID" value="<?php echo $_SESSION['user_id']; ?>">
        <label for="old_passwd" class="form-label">Old Password:</label>
        <input
          type="password"
          class="form-control"
          id="old_passwd"
          name="old_passwd"
          placeholder="Enter old password" required>
        </input>
        <span class='text-danger' id='old_passwd_val'></span>
      </div>
      <div class="mb-3">
        <label for="new_passwd" class="form-label">New Password:</label>
        <input
          type="password"
          class="form-control"
          id="new_passwd"
          name="new_passwd"
          placeholder="Enter new password" required>
        </input>
        <span class='text-danger' id='new_passwd_val'></span>
      </div>
      <div class="mb-3">
        <label for="new_passwd2" class="form-label">Re-Type New Password:</label>
        <input
          type="password"
          class="form-control"
          id="new_passwd2"
          name="new_passwd2"
          placeholder="Enter new password again" required>
        </input>
        <span class='text-danger' id='new_passwd2_val'></span>
      </div>
      <div class="mb-3 text-end">
          <button type="button"
                  class="btn btn-secondary"
                  onclick="window.location.href = './home.php'">Back</button>
          <button type="button" class="btn btn-primary" onclick="submitForm()">Submit</button>
      </div>
    </form>
  </div>

  <!-- Javascripts -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.js"></script>
  <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
  <script src="../js/update-password.js"></script>
</body>
</html>