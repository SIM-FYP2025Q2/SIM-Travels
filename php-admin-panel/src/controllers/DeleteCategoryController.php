<?php

require_once("/var/www/html/entity/VectorRepository.php");

class DeleteCategoryController
{
    private $vectorRepository;

    public function __construct()
    {
        $this->vectorRepository = new VectorRepository();
    }

    public function deleteCategory(int $id): bool
    {
        return $this->vectorRepository->deleteVectorsByCategory($id);
    }
}

/**
 * Script to handle the request of Delete Category
 * Expects a POST request with 'id'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' &&
    isset($_POST['id'])
){
    // Convert String ID to Integer
    $id = (int) $_POST['id'];

    // Instantiate Controller
    $deleteController = new DeleteCategoryController();
    $status = $deleteController->deleteCategory($id);

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