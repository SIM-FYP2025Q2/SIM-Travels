<?php

session_start();
if (isset($_SESSION['IS_LOGGED_IN'])) {
    // Redirecting to Home Page
    if ($_SESSION['is_admin']) {
        header("Location: ./view/admin.php");
        exit();
    } else {
        header("Location: ./view/home.php");
        exit();
    }
} else { ?>
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="../css/custom_bootstrap.css">
    <link rel="stylesheet" href="./css/login.css">
  </head>
  <body>
    <div class="container d-flex justify-content-center align-items-center min-vh-100">
      <div class="card p-4 shadow-lg" style="width: 100%; max-width: 400px;">
        <!-- Logo -->
        <div class="text-center mb-4">
          <img src="./img/icon-logo.png" alt="Logo" class="img-fluid" style="max-width: 100px;">
        </div>
        <h3 class="text-center mb-4">Login</h3>
        <!-- Error Message (as GET Value) -->
        <?php if(isset($_GET["error"])) {
          echo '<div class="alert alert-danger" role="alert">';
          echo htmlspecialchars($_GET["error"]);
          echo '</div>';
        } ?>
        <form id="loginForm" action="./controllers/LoginController.php" method="POST">
          <div class="mb-3">
            <label for="email" class="form-label">Email Address</label>
            <input type="email" class="form-control" id="email" placeholder="Enter email" name="email" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <div class="input-group">
              <input type="password" class="form-control" id="password" placeholder="Password" name="password" required />
              <button class="btn btn-outline-secondary" type="button" id="togglePassword"><ion-icon name="eye-outline"></ion-icon></button>
            </div>
          </div>
          <button type="submit" class="btn btn-primary w-100">Login</button>
        </form>
      </div>
    </div>
    <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
    <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
    <script src="./js/login.js"></script>
  </body>
  </html>
<?php } ?>