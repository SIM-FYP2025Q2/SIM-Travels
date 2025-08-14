<?php

require_once("/var/www/html/entity/UserAccount.php");

session_start();

class RegisterController
{
    private $ua;

    public function __construct()
    {
        $this->ua = new UserAccount();
    }
    
    public function createUserAccount(
        string $username,
        string $password,
        string $email
    ): bool {
        return $this->ua->createUserAccount($username, $password, $email);
    }
}

/**
 * Script to handle requests for creating user accounts
 * Expects a POST request with 'username', 'email', and 'password'.
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' &&
    isset($_POST['username']) &&
    isset($_POST['email']) &&
    isset($_POST['password'])
) {

    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = $_POST['password'];

    // Check if admin is logged in
    if (!isset($_SESSION['IS_LOGGED_IN']) || !isset($_SESSION['is_admin']) || $_SESSION['is_admin'] != 1) {
        echo json_encode(['success' => false, 'message' => 'Unauthorized access.']);
        exit();
    }

    // Basic input validation
    if (empty($username) || empty($email) || empty($password)) {
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'All fields are required.']);
        exit();
    }

    // Instantiate Controller and create user
    $registerController = new RegisterController();
    $status = $registerController->createUserAccount($username, $password, $email);

    if ($status) {
        header('Content-Type: application/json');
        echo json_encode(['success' => true, 'message' => 'User account created successfully.']);
        exit();
    } else {
        header('Content-Type: application/json');
        echo json_encode(['success' => false, 'message' => 'Failed to create user account.']);
        exit();
    }

    exit();
}