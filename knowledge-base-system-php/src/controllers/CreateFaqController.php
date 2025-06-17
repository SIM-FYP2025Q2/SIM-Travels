<?php

require_once("/var/www/html/entity/FaqRepository.php");

class CreateFaqController
{
    private $faq;

    public function __construct()
    {
        $this->faq = new FaqRepository();
    }
    
    public function createFaq(string $question, string $answer, int $category_id, ?string $link): bool
    {
        return $this->faq->createFaq($question, $answer, $category_id, $link);
    }
}

/**
 * Script to handle the request of Update FAQ.
 * Expects a POST request with 'question', 'answer', 'category_id', and optional 'link'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' && 
    isset($_POST['question']) && 
    isset($_POST['answer']) && 
    isset($_POST['category_id'])
){
    $question = $_POST['question'];
    $answer = $_POST['answer'];
    $category_id = (int) $_POST['category_id'];
    $link = isset($_POST['link']) ? $_POST['link'] : null;

    // Instantiate Controller
    $createController = new CreateFaqController();
    $status = $createController->createFaq($id, $question, $answer, $category_id, $link);

    // Parse Success/Fail Response
    if ($status) {
        header("Location: ../view/create.php?status=1");
        exit();
    } else {
        header("Location: ../view/create.php?status=0");
        exit();
    }

    // Send Response as JSON
    header('Content-Type: application/json');
    echo json_encode($response);
    exit();
}