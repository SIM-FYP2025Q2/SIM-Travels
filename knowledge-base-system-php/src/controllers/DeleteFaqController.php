<?php

require_once("/var/www/html/entity/FaqRepository.php");

class DeleteFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }

    public function deleteFaq(int $id): bool
    {
        return $this->faq->deleteFaq($id);
    }
}

/**
 * Script to handle the request of Delete FAQ.
 * Expects a POST request with 'id'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['id'])) {
    // Convert String ID to Integer
    $id = (int) $_POST['id'];

    // Instantiate Controller
    $deleteController = new DeleteFaqController();
    $status = $deleteController->deleteFaq($id);

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