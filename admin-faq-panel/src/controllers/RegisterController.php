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
 * Script to handle the Login Request.
 * Expects a POST request with 'email' and 'password'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' && 
    isset($_POST['username']) && 
    isset($_POST['email']) && 
    isset($_POST['password'])
) {
    // Instantiate Controller
    $createController = new RegisterController();
    $status = $createController-> createUserAccount(
        $_POST['username'],
        $_POST['password'],
        $_POST['email']
    );

    if ($status) {
        header("Location: ../register.php?status=Success, please wait for admin approval");
        exit();
    } else {
        header("Location: ../register.php?status=Error Username or Email already Exists");
        exit();
    }
}