<?php

require_once("/var/www/html/entity/FaqRepository.php");

class UpdateFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }
    
    public function updateFaq(int $id, string $question, string $answer, int $category_id, ?string $link): bool
    {
        return $this->faq->updateFaq($id, $question, $answer, $category_id, $link);
    }
}

/**
 * Script to handle the request of Update FAQ.
 * Expects a POST request with 'id', 'question', 'answer', 'category_id', and optional 'link'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' && 
    isset($_POST['id']) && 
    isset($_POST['question']) && 
    isset($_POST['answer']) && 
    isset($_POST['category_id'])
){
    // Convert String IDs to Integer
    $id = (int) $_POST['id'];
    $question = $_POST['question'];
    $answer = $_POST['answer'];
    $category_id = (int) $_POST['category_id'];
    $link = isset($_POST['link']) ? $_POST['link'] : null;

    // Instantiate Controller
    $updateController = new UpdateFaqController();
    $status = $updateController->updateFaq($id, $question, $answer, $category_id, $link);

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