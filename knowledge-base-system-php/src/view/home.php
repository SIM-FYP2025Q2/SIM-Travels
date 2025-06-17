<?php

session_start();

require_once("../controllers/ViewAllFaqController.php");
require_once("../controllers/SearchFaqController.php");
require_once("../controllers/GetFaqCategoriesController.php");

if (!isset($_SESSION['IS_LOGGED_IN'])) {
    // Redirecting to Login Page
    header("Location: ../login.php");
    exit();
}

// Check if GET['id'] Parameter Exists
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

      // Search FAQ Entries
      $controller = new SearchFaqController();
      $faqItems = $controller->searchFaq($searchTerm);
    }
} else {
    // Read All FAQ Entries
    $controller = new ViewAllFaqController();
    $faqItems = $controller->readAllFaq();
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

  <!-- Sync Modal -->
  <div 
    class="modal fade" 
    id="syncModal"
    tabindex="-1"
    aria-labelledby="SyncModalLabel"
    aria-hidden="true"
    data-bs-backdrop="static"
    data-bs-keyboard="false">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="SyncModalLabel">Sync to PineconeDB</h1>
        </div>
        <div class="modal-body">
          <div class="alert alert-warning">Warning! Do not close/reload page ...</div>
        </div>
      </div>
    </div>
  </div>

  <!-- View Modal -->
  <div class="modal fade" id="viewFaqModal" tabindex="-1" aria-labelledby="ViewFaqModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="ViewFaqModalLabel">FAQ Info</h1>
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

  <!-- Update Modal -->
  <div class="modal fade" id="updateFaqModal" tabindex="-1" aria-labelledby="ViewFaqModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="ViewFaqModalLabel">FAQ Info</h1>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form id="updateFaqForm">
            <input type="hidden" id="faqId" name="id" value="">
            <div class="mb-3">
              <label for="u_question" class="form-label">Question</label>
              <textarea class="form-control" id="u_question" name="question" rows="2"></textarea>
            </div>
            <div class="mb-3">
              <label for="u_answer" class="form-label">Answer</label>
              <textarea class="form-control" id="u_answer" name="answer" rows="5"></textarea>
            </div>
            <div class="mb-3">
              <label for="u_category" class="form-label">Category</label>
              <select class="form-select" id="u_category" name="category">
                <?php foreach ($faqCategories as $category): ?>
                  <option value="<?php echo htmlspecialchars($category['id']); ?>">
                    <?php echo htmlspecialchars($category['category']); ?>
                  </option>
                <?php endforeach; ?>
              </select>
            </div>
            <div class="mb-3">
              <label for="u_link" class="form-label">Link (Optional)</label>
              <input type="text" class="form-control" id="u_link" name="link"/>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary" onclick="updateFaqForm()">Save changes</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Knowledge Base Content Section -->
  <div class="container mt-4">
    <!-- Search Bar -->
    <div class="d-flex justify-content-between align-items-center mb-4 w-100">
      <div class="input-group d-flex me-3 w-75">
          <span class="input-group-text">
              <ion-icon name="search-outline"></ion-icon>
          </span>
          <input type="text" class="form-control" placeholder="Search by Question/Category ..." id="search_term">
          <button class="btn btn-primary" type="button" onclick="searchBtnClicked()">Search</button>
      </div>
      <!-- Create Button -->
      <div class="d-flex gap-2">
          <button
            class="btn btn-success d-flex align-items-center gap-1" 
            data-bs-toggle="modal"
            data-bs-target="#syncModal"
            onclick="syncFaq()",
            id="syncBtn">
              <ion-icon name="sync-outline" style="font-size: 1.2rem;"></ion-icon>
              <span>Sync</span>
          </button>
          <button class="btn btn-primary d-flex align-items-center gap-1" 
                  id="createBtn"
                  onclick="window.location.href = './create.php'">
              <ion-icon name="add-outline" style="font-size: 1.2rem;"></ion-icon>
              <span>Create</span>
          </button>
      </div>
  </div>

  <!-- Table -->
  <div class="table-responsive">
    <table class="table table-hover table-striped align-middle border shadow-sm px-4 py-2">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Question</th>
          <th scope="col">Category</th>
          <th scope="col">Synced</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody id="kbTable">
        <?php foreach ($faqItems as $f): ?>
          <tr>
              <td><?php echo htmlspecialchars($f->getId()); ?></td>
              <td class="col-4 text-truncate"><?php echo htmlspecialchars($f->getQuestion()); ?></td>
              <td class="col-2"><?php echo htmlspecialchars($f->getCategory()); ?></td>
              <td>
                <?php
                  if ($f->is_synced()) {
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
                  data-bs-target="#viewFaqModal"
                  onclick="viewFaq('<?php echo $f->getId(); ?>')">
                    <span class="d-flex align-items-center gap-2">
                      <ion-icon name="eye" style="font-size: 1rem;"></ion-icon>
                      View
                    </span>
                </button>
                <button 
                  class="btn btn-outline-warning btn-sm mb-1"
                  data-bs-toggle="modal"
                  data-bs-target="#updateFaqModal"
                  onclick="updateFaq('<?php echo $f->getId(); ?>')">
                    <span class="d-flex align-items-center gap-2">
                      <ion-icon name="options" style="font-size: 1rem;"></ion-icon>
                      Update
                    </span>
                </button>
                <button 
                  class="btn btn-outline-danger btn-sm mb-1"
                  onclick="deleteFaq('<?php echo $f->getId(); ?>')">
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
  <script src="../js/home.js"></script>
</body>
</html>