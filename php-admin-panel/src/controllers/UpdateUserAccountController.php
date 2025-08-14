<?php

require_once("/var/www/html/entity/UserAccount.php");

class UpdateUserAccountController
{
    private $userAccount;

    public function __construct()
    {
        $this->userAccount = new UserAccount();
    }
    
    public function updateUserAccount(int $id, string $username, string $email, ?string $password, int $isAdmin, int $isActive): bool
    {
        return $this->userAccount->updateUserAccount($id, $username, $email, $password, $isAdmin, $isActive);
    }
}

/**
 * Script to handle the request of Update User Account.
 * Expects a POST request with 'id', 'username', 'email', 'is_admin', and 'is_active'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' && 
    isset($_POST['id']) && 
    isset($_POST['username']) && 
    isset($_POST['email']) && 
    isset($_POST['is_admin']) && 
    isset($_POST['is_active']) &&
    isset($_POST['password'])
) {
    // Convert String IDs to Integer
    $id = (int) $_POST['id'];
    $username = $_POST['username'];
    $email = $_POST['email'];
    $isAdmin = (int) $_POST['is_admin'];
    $isActive = (int) $_POST['is_active'];
    $password = !empty($_POST['password']) ? $_POST['password'] : null;

    // Instantiate Controller
    $updateController = new UpdateUserAccountController();
    $status = $updateController->updateUserAccount($id, $username, $email, $password, $isAdmin, $isActive);

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