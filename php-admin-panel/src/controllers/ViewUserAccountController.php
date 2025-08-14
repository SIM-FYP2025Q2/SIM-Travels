<?php

require_once("/var/www/html/entity/UserAccount.php");

class ViewUserAccountController
{
    private $userAccount;

    public function __construct()
    {
        $this->userAccount = new UserAccount();
    }

    public function readUserAccount(int $id): ?UserAccount
    {
        return $this->userAccount->getUserById($id);
    }
}

/**
 * Script to handle the request of View User Account.
 * Expects a GET request with 'id'
 */
if (isset($_GET['id'])) {
    // Convert String ID to Integer
    $id = (int) $_GET['id'];

    // Instantiate Controller
    $viewController = new ViewUserAccountController();
    $user = $viewController->readUserAccount($id);

    // Error Getting User
    if (is_null($user)) {
        echo json_encode(['error' => 'Invalid request']);
        exit();
    }

    // Parse & Send Response as JSON
    $response = [
        'id' => $user->getId(),
        'username' => $user->getUsername(),
        'email' => $user->getEmail(),
        'is_admin' => $user->isAdmin(),
        'is_active' => $user->isActive(),
    ];
    header('Content-Type: application/json');
    echo json_encode($response);
    exit();
}