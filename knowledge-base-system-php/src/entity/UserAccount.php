<?php

require_once("Database.php");

class UserAccount
{
    protected int $id;              // ID of Account
    protected string $username;     // Username (Unique)
    protected string $password;     // Password Hashed
    protected string $email;        // Email (Unique)
    protected int $is_admin;        // Account is Admin
    protected int $is_active;       // Account is Activated

    // CRUD Operations //

    /**
     * Creates a New User Account
     *
     * @param string $username      Username
     * @param string $password      Password
     * @param string $email         Email
     *
     * @return bool Returns true if Create Operation Success, Else false
    */
    public function createUserAccount(
        string $username,
        string $password,
        string $email
    ): bool {
        
        $db_conn = Database::getConnection();
        
        // Hash Password
        $passwd = password_hash($password, PASSWORD_DEFAULT);
        
        // SQL TryCatch Statement
        try {
            // Bind Paramaters & Execute Statement
            $sql = "INSERT INTO `Users` (`username`, `email`, `password`)
                    VALUES (:username, :email, :password)";
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':username', $username);
            $stmt->bindParam(':password', $passwd);
            $stmt->bindParam(':email', $email);
            $execResult = $stmt->execute();

            // If Success, return true, else return false
            if ($execResult) {
                return true;
            } else {
                return false;
            }
        } catch (PDOException $e) {
            error_log("Database insert failed: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Logins a User Account, Checks if UserAccount Exists, with Valid Password
     *
     * @param string $email         Input Email
     * @param string $password      Input Password
     *
     * @return ?UserAccount Return UserAccount Object is Success, null otherwise
    */
    public function login(string $email, string $password): ?UserAccount
    {
        // SQL Statement (+ Checks user profile isSuspend status)
        // Returns NULL if Invalid Password / No Users Found

        $db_conn = Database::getConnection();

        try {
            // Execute Statement for UserAccount
            $sql = "SELECT * FROM `Users`
                    WHERE `email` = :email";
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':email', $email);
            $stmt->execute();
            
            // Ensure Only 1 Row
            if ($stmt->rowCount() == 1) {
                // Retrieve User Account
                $userAccount = $stmt->fetchObject('UserAccount');
            } else {
                return null;
            }

            // Verify Password
            if (password_verify($password, $userAccount->getPassword())) {
                return $userAccount;
            } else {
                error_log("Password verify failed");
                return null;
            }
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return null;
        }
    }

    // Accessor Methods
    public function getId(): int
    {
        return $this->id;
    }

    public function getUsername(): string
    {
        return $this->username;
    }

    public function getPassword(): string
    {
        return $this->password;
    }

    public function getEmail(): string
    {
        return $this->email;
    }
    
    public function isActive(): bool
    {
        return $this->is_active == 1 ? true : false;
    }
}