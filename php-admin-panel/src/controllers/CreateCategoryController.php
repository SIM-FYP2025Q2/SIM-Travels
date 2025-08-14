<?php

require_once("/var/www/html/entity/FaqRepository.php");

class CreateCategoryController
{
    private $faqRepository;

    public function __construct()
    {
        $this->faqRepository = new FaqRepository();
    }

    public function createCategory(string $categoryName): bool
    {
        return $this->faqRepository->createCategory($categoryName);
    }
}

/**
 * Script to handle the request of Create Category.
 * Expects a POST request with 'category_name'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' &&
    isset($_POST['category_name'])
){
    // Get Category Name
    $categoryName = $_POST['category_name'];

    // Instantiate Controller
    $createController = new CreateCategoryController();
    $status = $createController->createCategory($categoryName);


    // Parse Success/Fail Response
    if ($status) {
        $response = [
            'isSuccess' => true,
        ];
    } else {
        $response = [
            'isSuccess' => false,
        ];
    }

    // Send Response as JSON
    header('Content-Type: application/json');
    echo json_encode($response);
    exit();
}
