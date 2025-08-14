<?php

session_start();

require_once("/var/www/html/entity/UserAccount.php");

class UpdatePasswordController
{
    private $userAccount;

    public function __construct()
    {
        $this->userAccount = new UserAccount();
    }

    public function updatePassword(int $userID, string $oldPassword, string $newPassword): int
    {
        return $this->userAccount->updatePassword($userID, $oldPassword, $newPassword);
    }
}

/**
 * Script to handle the request of Update Password.
 * Expects a POST request with 'userID', 'old_passwd', 'new_passwd', 'new_passwd2'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get form data
    $userID = (int) $_POST['userID'];
    $oldPassword = $_POST['old_passwd'];
    $newPassword = $_POST['new_passwd'];
    $newPassword2 = $_POST['new_passwd2'];

    // Basic validation
    if ($newPassword !== $newPassword2) {
        // Passwords do not match
        header("Location: ../view/update-password.php?status=0");
        exit();
    }

    // Check if user is trying to update their own password
    if (!isset($_SESSION['user_id']) || $_SESSION['user_id'] != $userID) {
        // Prevent users from updating other users' passwords
        header("Location: ../view/update-password.php?status=0");
        exit();
    }

    // Instantiate Controller
    $controller = new UpdatePasswordController();
    $result = $controller->updatePassword($userID, $oldPassword, $newPassword);

    if ($result == 1) {
        // Success
        header("Location: ../view/update-password.php?status=1");
        exit();
    } else if ($result == 0) {
        // Incorrect Password
        header("Location: ../view/update-password.php?status=0");
        exit();
    } else {
        // Failure
        header("Location: ../view/update-password.php?status=-1");
        exit();
    }
} else {
    // If not a POST request, redirect to home
    header("Location: ../view/home.php");
    exit();
}