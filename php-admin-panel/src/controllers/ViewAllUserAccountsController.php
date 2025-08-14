<?php

require_once("/var/www/html/entity/UserAccount.php");

class ViewAllUserAccountsController
{
    private $userAccount;

    public function __construct()
    {
        $this->userAccount = new UserAccount();
    }

    public function readAllUserAccounts(): array
    {
        return $this->userAccount->getAllUsers();
    }
}