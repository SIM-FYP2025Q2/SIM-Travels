<?php

require_once("/var/www/html/entity/VectorRepository.php");

class SyncFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new VectorRepository();
    }
    
    public function upsertVectors(): bool
    {
        return $this->faq->upsertVectors();
    }
}

/**
 * Script to handle the request of Update FAQ.
 * Expects a GET Request
 */
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['sync'])) {

    // Instantiate Controller
    $syncController = new SyncFaqController();
    $status = $syncController->upsertVectors();

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