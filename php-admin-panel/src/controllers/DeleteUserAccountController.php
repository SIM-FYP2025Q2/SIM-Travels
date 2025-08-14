<?php

require_once("/var/www/html/entity/UserAccount.php");

class DeleteUserAccountController
{
    private $userAccount;

    public function __construct()
    {
        $this->userAccount = new UserAccount();
    }

    public function deleteUserAccount(int $id): bool
    {
        return $this->userAccount->deleteUserAccount($id);
    }
}

/**
 * Script to handle the request of Delete User Account.
 * Expects a POST request with 'id'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' &&
    isset($_POST['id'])
) {
    // Convert String ID to Integer
    $id = (int) $_POST['id'];

    // Instantiate Controller
    $deleteController = new DeleteUserAccountController();
    $status = $deleteController->deleteUserAccount($id);

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