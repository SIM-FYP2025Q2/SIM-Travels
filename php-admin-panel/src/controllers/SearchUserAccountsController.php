<?php

require_once("/var/www/html/entity/UserAccount.php");

class SearchUserAccountsController
{
    private $userAccount;

    public function __construct()
    {
        $this->userAccount = new UserAccount();
    }

    public function searchUserAccounts(string $searchTerm): array
    {
        return $this->userAccount->searchUsers($searchTerm);
    }
}