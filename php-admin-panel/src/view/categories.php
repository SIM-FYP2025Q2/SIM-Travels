<?php

session_start();

require_once("../controllers/GetFaqCategoriesController.php");
require_once("../controllers/SearchCategoryController.php");
require_once("../controllers/CreateCategoryController.php");
require_once("../controllers/DeleteCategoryController.php");

if (!isset($_SESSION['IS_LOGGED_IN'])) {
    // Redirecting to Login Page
    header("Location: ../login.php");
    exit();
}

// Check if the user is an admin
if ($_SESSION['is_admin'] == 1) {
    // Redirect to an admin page
    header("Location: admin.php");
    exit();
}

// Handle category deletion
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete_category_id'])) {
    $categoryId = (int)$_POST['delete_category_id'];
    $controller = new DeleteCategoryController();
    if ($controller->deleteCategory($categoryId)) {
        $_SESSION['message'] = "Category and associated FAQs deleted successfully!";
        $_SESSION['message_type'] = "success";
    } else {
        $_SESSION['message'] = "Failed to delete category.";
        $_SESSION['message_type'] = "danger";
    }
    header("Location: categories.php");
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

      // Search Category Entries
      $controller = new SearchCategoryController();
      $categories = $controller->searchCategories($searchTerm);
    }
} else {
    // Read All Category Entries
    $controller = new GetFaqCategoriesController();
    $categories = $controller->readAllFaqCategories();
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Categories</title>
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
            <a class="nav-link active" aria-current="page" href="categories.php">Categories</a>
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
            <li><a class="dropdown-item" href="update-password.php">Change Password</a></li>
            <li><a class="dropdown-item" href="../logout.php">Logout</a></li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <!-- Main Content Section -->
  <div class="container mt-4">

    <!-- Search Bar and Create Button -->
    <div class="d-flex justify-content-between align-items-center mb-4 w-100">
      <div class="input-group d-flex me-3 w-75">
          <span class="input-group-text">
              <ion-icon name="search-outline"></ion-icon>
          </span>
          <input type="text" class="form-control" placeholder="Search by Category Name ..." id="search_term">
          <button class="btn btn-primary" type="button" onclick="searchBtnClicked()">Search</button>
      </div>
      <!-- Create Button -->
      <div class="d-flex gap-2">
          <button class="btn btn-primary d-flex align-items-center gap-1"
                  data-bs-toggle="modal"
                  data-bs-target="#createCategoryModal">
              <ion-icon name="add-outline" style="font-size: 1.2rem;"></ion-icon>
              <span>Create Category</span>
          </button>
      </div>
    </div>

    <!-- Create Category Modal -->
    <div class="modal fade" id="createCategoryModal" tabindex="-1" aria-labelledby="createCategoryModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="createCategoryModalLabel">Create New Category</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <form id="createCategoryForm">
            <div class="modal-body">
              <div class="mb-3">
                <label for="category_name" class="form-label">Category Name</label>
                <input type="text" class="form-control" id="category_name" name="category_name" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" onclick="createCategory()">Create</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-responsive">
      <table class="table table-hover table-striped align-middle border shadow-sm px-4 py-2">
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Category Name</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody id="categoryTable">
          <?php if (!empty($categories)): ?>
            <?php foreach ($categories as $category): ?>
              <tr>
                  <td><?php echo htmlspecialchars($category['id']); ?></td>
                  <td><?php echo htmlspecialchars($category['category']); ?></td>
                  <td class="text-end">
                    <button
                      class="btn btn-outline-danger btn-sm mb-1"
                      onclick="deleteCategory('<?php echo htmlspecialchars($category['id']); ?>')">
                        <span class="d-flex align-items-center gap-2">
                          <ion-icon name="trash" style="font-size: 1rem;"></ion-icon>
                          Delete
                        </span>
                    </button>
                  </td>
              </tr>
            <?php endforeach; ?>
          <?php else: ?>
            <tr>
                <td colspan="3" class="text-center">No categories found.</td>
            </tr>
          <?php endif; ?>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Javascripts -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/js/bootstrap.bundle.js"></script>
  <script type="module" src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.esm.js"></script>
  <script nomodule src="https://unpkg.com/ionicons@7.1.0/dist/ionicons/ionicons.js"></script>
  <script src="../js/categories.js"></script>
</body>
</html>
