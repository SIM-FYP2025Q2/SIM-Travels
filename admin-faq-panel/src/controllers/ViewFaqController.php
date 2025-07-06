<?php

require_once("/var/www/html/entity/FaqRepository.php");

class ViewFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }

    public function readFaq(int $id): ?FaqRepository
    {
        return $this->faq->readFaq($id);
    }
}

/**
 * Script to handle the request of View Shortlist.
 * Expects a GET request with 'id' and 'serviceID'
 */
if (isset($_GET['id'])) {
    // Convert String IDs to Integer
    $id = (int) $_GET['id'];

    // Instantiate Controller
    $viewController = new ViewFaqController();
    $faq = $viewController->readFaq($id);

    // Error Getting Service
    if (is_null($faq)) {
        echo json_encode(['error' => 'Invalid request']);
        exit();
    }

    // Parse & Send Response as JSON
    $response = [
        'id' => $faq->getId(),
        'question' => $faq->getQuestion(),
        'answer' => $faq->getAnswer(),
        'category' => $faq->getCategoryId(),
        'link' => $faq->getLink(),
    ];
    header('Content-Type: application/json');
    echo json_encode($response);
    exit();
}