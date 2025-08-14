<?php

session_start();

require_once("../controllers/ViewAllUserAccountsController.php");
require_once("../controllers/SearchUserAccountsController.php");

if (!isset($_SESSION['IS_LOGGED_IN'])) {
    // Redirecting to Login Page
    header("Location: ../login.php");
    exit();
}

// Check if the user is an admin
if ($_SESSION['is_admin'] != 1) {
    // Redirect to a non-admin page or show an error
    header("Location: home.php"); // Redirect to the FAQ homepage
    exit();
}

// Check if GET['q'] Parameter Exists for search
if (isset($_GET['q'])) {
    if ($_GET['q'] != '') {
      // Remove Quotes, URL Decode, Trim Consecutive/Trailing Whitespaces
      $searchTerm = str_replace(['"', "'"], '', $_GET['q']);

      // URL Decode
      $searchTerm = urldecode($searchTerm);

      // Trim Consecutive/Trailing Whitespaces
      $searchTerm = preg_replace('/\s{2,}/', ' ', $searchTerm);
      $searchTerm = ltrim($searchTerm);
      $searchTerm = rtrim($searchTerm);

      // Search User Accounts
      $controller = new SearchUserAccountsController();
      $userAccounts = $controller->searchUserAccounts($searchTerm);
    }
} else {
    // Read All User Accounts
    $controller = new ViewAllUserAccountsController();
    $userAccounts = $controller->readAllUserAccounts();
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>User Management</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.css" rel="stylesheet">
  <link rel="stylesheet" href="../css/custom_bootstrap.css" />
</head>
<body>

  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg bg-light border-bottom shadow-sm px-4 py-2">
    <div class="container-fluid">
      <!-- Brand Logo -->
      <a class="navbar-brand" href="home.php">
        <img src="../img/icon-logo.png" alt="Logo" height="32">
      </a>
      <!-- Page Links -->
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" aria-current="page" href="admin.php">Knowledge Base</a>
          </li>
          <?php if (isset($_SESSION['is_admin']) && $_SESSION['is_admin'] == 1): ?>
          <li class="nav-item">
            <a class="nav-link active" href="admin.php">User Management</a>
          </li>
          <?php endif; ?>
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

  <!-- View User Modal -->
  <div class="modal fade" id="viewUserModal" tabindex="-1" aria-labelledby="ViewUserModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="ViewUserModalLabel">User Info</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form>
            <fieldset disabled>
              <div class="mb-3">
                <label for="r_username" class="form-label">Username</label>
                <input type="text" class="form-control" id="r_username"/>
              </div>
              <div class="mb-3">
                <label for="r_email" class="form-label">Email</label>
                <input type="email" class="form-control" id="r_email"/>
              </div>
              <div class="mb-3">
                <label for="r_is_admin" class="form-label">Is Admin</label>
                <input type="text" class="form-control" id="r_is_admin"/>
              </div>
              <div class="mb-3">
                <label for="r_is_active" class="form-label">Is Active</label>
                <input type="text" class="form-control" id="r_is_active"/>
              </div>
            </fieldset>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Update User Modal -->
  <div class="modal fade" id="updateUserModal" tabindex="-1" aria-labelledby="UpdateUserModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="UpdateUserModalLabel">Update User</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="updateUserForm">
            <input type="hidden" id="userId" name="id" value="">
            <div class="mb-3">
              <label for="u_username" class="form-label">Username</label>
              <input
                type="text" class="form-control" id="u_username" name="username" placeholder="Enter new username"/>
            </div>
            <div class="mb-3">
              <label for="u_email" class="form-label">Email</label>
              <input type="email" class="form-control" id="u_email" name="email" placeholder="Enter new email"/>
            </div>
            <div class="mb-3">
              <label for="u_password" class="form-label">Password</label>
              <input 
                type="password"
                class="form-control"
                id="u_password"
                name="password"
                placeholder="Leave blank to keep current password"/>
            </div>
            <div class="mb-3">
              <label for="u_is_admin" class="form-label">Is Admin</label>
              <select class="form-select" id="u_is_admin" name="is_admin">
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="u_is_active" class="form-label">Is Active</label>
              <select class="form-select" id="u_is_active" name="is_active">
                <option value="1">Yes</option>
                <option value="0">No</option>
              </select>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" onclick="updateUserForm()">Save changes</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Create User Modal -->
  <div class="modal fade" id="createUserModal" tabindex="-1" aria-labelledby="CreateUserModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="CreateUserModalLabel">Create New User</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="createUserForm">
            <div class="mb-3">
              <label for="c_username" class="form-label">Username</label>
              <input type="text" class="form-control" id="c_username" name="username" placeholder="Enter username" required/>
            </div>
            <div class="mb-3">
              <label for="c_email" class="form-label">Email</label>
              <input type="email" class="form-control" id="c_email" name="email" placeholder="Enter email" required/>
            </div>
            <div class="mb-3">
              <label for="c_password" class="form-label">Password</label>
              <input type="password" class="form-control" id="c_password" name="password" placeholder="Enter password" required/>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" onclick="createUser()">Create User</button>
        </div>
      </div>
    </div>
  </div>

  <!-- User Management Content Section -->
  <div class="container mt-4">
    <!-- Search Bar -->
    <div class="d-flex justify-content-between align-items-center mb-4 w-100">
      <div class="input-group d-flex me-3 w-75">
          <span class="input-group-text">
              <ion-icon name="search-outline"></ion-icon>
          </span>
          <input type="text" class="form-control" placeholder="Search by Username/Email ..." id="search_term">
          <button class="btn btn-primary" type="button" onclick="searchUserAccounts()">Search</button>
      </div>
      <!-- Create Button -->
      <div class="d-flex gap-2">
          <button
            class="btn btn-success d-flex align-items-center gap-1"
            data-bs-toggle="modal"
            data-bs-target="#createUserModal">
              <ion-icon name="add-outline" style="font-size: 1.2rem;"></ion-icon>
              <span>Create User</span>
          </button>
      </div>
  </div>

  <!-- Table -->
  <div class="table-responsive">
    <table class="table table-hover table-striped align-middle border shadow-sm px-4 py-2">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Username</th>
          <th scope="col">Email</th>
          <th scope="col">Is Admin</th>
          <th scope="col">Is Active</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody id="userTable">
        <?php foreach ($userAccounts as $user): ?>
          <tr>
              <td><?php echo htmlspecialchars($user->getId()); ?></td>
              <td><?php echo htmlspecialchars($user->getUsername()); ?></td>
              <td><?php echo htmlspecialchars($user->getEmail()); ?></td>
              <td>
                <?php
                  if ($user->isAdmin()) {
                    echo '<span class="text-primary"><b>Yes</b></span>';
                  } else {
                    echo '<span class="text-danger"><b>No</b></span>';
                  }
                ?>
              </td>
              <td>
                <?php
                  if ($user->isActive()) {
                    echo '<span class="text-primary"><b>Yes</b></span>';
                  } else {
                    echo '<span class="text-danger"><b>No</b></span>';
                  }
                ?>
              </td>
              <td class="text-end">
                <button
                  class="btn btn-outline-info btn-sm mb-1"
                  data-bs-toggle="modal"
                  data-bs-target="#viewUserModal"
                  onclick="viewUser('<?php echo $user->getId(); ?>')">
                    <span class="d-flex align-items-center gap-2">
                      <ion-icon name="eye" style="font-size: 1rem;"></ion-icon>
                      View
                    </span>
                </button>
                <button
                  class="btn btn-outline-warning btn-sm mb-1"
                  data-bs-toggle="modal"
                  data-bs-target="#updateUserModal"
                  onclick="updateUser('<?php echo $user->getId(); ?>')">
                    <span class="d-flex align-items-center gap-2">
                      <ion-icon name="options" style="font-size: 1rem;"></ion-icon>
                      Update
                    </span>
                </button>
                <button
                  class="btn btn-outline-danger btn-sm mb-1"
                  onclick="deleteUser('<?php echo $user->getId(); ?>')">
                    <span class="d-flex align-items-center gap-2">
                      <ion-icon name="trash" style="font-size: 1rem;"></ion-icon>
                      Delete
                    </span>
                </button>
              </td>
          </tr>
        <?php endforeach; ?>
      </tbody>
    </table>
  </div>

  <!-- Javascripts -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.js"></script>
  <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
  <script src="../js/admin.js"></script>
</body>
</html>