<?php

require_once("/var/www/html/entity/UserAccount.php");

session_start();

class LoginController
{
    private $ua;

    public function __construct()
    {
        $this->ua = new UserAccount();
    }
    
    public function login(string $email, string $password): ?UserAccount
    {
        return $this->ua->login($email, $password);
    }
}

/**
 * Script to handle the Login Request.
 * Expects a POST request with 'email' and 'password'
 */
if ($_SERVER['REQUEST_METHOD'] === 'POST' && 
    isset($_POST['email']) && 
    isset($_POST['password'])
) {
    
    // Instantiate Controller
    $loginController = new LoginController();
    $userAccount = $loginController->login($_POST['email'], $_POST['password']);

    // Null User: Display Invalid Credentials Error
    if (is_null($userAccount)) {
        header("Location: ../login.php?error=Invalid Credentials");
        exit();
    // Suspended User: Display User Suspended Error
    } elseif ($userAccount->isActive()) {
        // Set Session Variables
        $_SESSION['IS_LOGGED_IN'] = true;
        $_SESSION['username'] = $userAccount->getUsername();
        $_SESSION['is_admin'] = $userAccount->isAdmin();
        $_SESSION['user_id'] = $userAccount->getId();

        // Redirecting to Home Page
        if ($userAccount->isAdmin()) {
            header("Location: ../view/admin.php");
            exit();
        } else {
            header("Location: ../view/home.php");
            exit();
        }
    } else {
        header("Location: ../login.php?error=User Suspended");
        exit();
    }
} else {
    header("Location: ../login.php?error=Unexpected Error Occured");
    exit();
}