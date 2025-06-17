<?php

session_start();

require_once("../controllers/GetFaqCategoriesController.php");

if (!isset($_SESSION['IS_LOGGED_IN'])) {
    // Redirecting to Login Page
    header("Location: ../login.php");
    exit();
}

// Get All FAQ Categories
$categoryController = new GetFaqCategoriesController();
$faqCategories = $categoryController->readAllFaqCategories();
?>


<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Homepage</title>
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
            <a class="nav-link active" aria-current="page" href="home.php">Knowledge Base</a>
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
            <!-- <li><a class="dropdown-item" href="#">Change Password</a></li> -->
            <li><a class="dropdown-item" href="../logout.php">Logout</a></li>
          </ul>
        </div>
      </div>
    </div>
  </nav>

  <!-- View Modal -->
  <div class="modal fade" id="viewFaqModal" tabindex="-1" aria-labelledby="ViewFaqModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="exampleModalLabel">FAQ Info</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form>
            <fieldset disabled>
              <div class="mb-3">
                <label for="r_question" class="form-label">Question</label>
                <textarea class="form-control" id="r_question" rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label for="r_answer" class="form-label">Answer</label>
                <textarea class="form-control" id="r_answer" rows="5"></textarea>
              </div>
              <div class="mb-3">
                <label for="r_category" class="form-label">Category</label>
                <select class="form-select" id="r_category" name="category">
                  <?php foreach ($faqCategories as $category): ?>
                    <option value="<?php echo htmlspecialchars($category['id']); ?>">
                      <?php echo htmlspecialchars($category['category']); ?>
                    </option>
                  <?php endforeach; ?>
                </select>
              </div>
              <div class="mb-3">
                <label for="r_link" class="form-label">Link</label>
                <input type="text" class="form-control" id="r_link"/>
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

  <!-- Create Form -->
  <div class="container mt-4">
    <h2>Create FAQ Entry</h3>
    <hr/>
  </div>
  <div class="container-lg card p-4 shadow-lg">
    <?php
      if (isset($_GET['status'])) {
        if ($_GET['status'] == 1) {
          echo '<div class="alert alert-success" role="alert">';
          echo 'Successfully created FAQ Entry!';
          echo '</div>';
        } else {
          echo '<div class="alert alert-danger" role="alert">';
          echo 'Unable to create FAQ Entry, please try again later.';
          echo '</div>';
        }
      }
    ?>
    <form id="createFaqForm" action="../controllers/CreateFaqController.php" method="POST">
      <div class="mb-3">
        <label for="question" class="form-label">Question</label>
        <textarea
          class="form-control"
          rows="2"
          id="question"
          name="question"
          placeholder="Question ..." required></textarea>
        <span class='text-danger' id='question_val'></span>
      </div>
      <div class="mb-3">
        <label for="answer" class="form-label">Answer</label>
        <textarea
          class="form-control"
          rows="5"
          id="answer"
          name="answer"
          placeholder="Answer ..." required></textarea>
        <span class='text-danger' id='answer_val'></span>
      </div>
      <div class="mb-3">
        <label for="category_id" class="form-label">Category</label>
        <select class="form-select" id="category_id" name="category_id">
          <?php foreach ($faqCategories as $category): ?>
            <option value="<?php echo htmlspecialchars($category['id']); ?>">
              <?php echo htmlspecialchars($category['category']); ?>
            </option>
          <?php endforeach; ?>
        </select>
      </div>
      <div class="mb-3">
        <label for="link" class="form-label">Link (Optional)</label>
        <input type="url" class="form-control" id="link" name="link" placeholder="https://example.com"/>
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
  <script src="../js/create.js"></script>
</body>
</html>