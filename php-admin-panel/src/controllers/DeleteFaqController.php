<?php

require_once("/var/www/html/entity/VectorRepository.php");

class DeleteFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new VectorRepository();
    }

    public function deleteVector(int $id, int $is_synced): bool
    {
        return $this->faq->deleteVector($id, $is_synced);
    }
}

/**
 * Script to handle the request of Delete FAQ.
 * Expects a POST request with 'id'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' &&
    isset($_POST['id']) &&
    isset($_POST['is_synced'])
){
    // Convert String ID to Integer
    $id = (int) $_POST['id'];
    $is_synced = (int) $_POST['is_synced'];

    // Instantiate Controller
    $deleteController = new DeleteFaqController();
    $status = $deleteController->deleteVector($id, $is_synced);

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