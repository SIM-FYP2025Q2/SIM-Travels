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

    /**
     * Retrieves all User Accounts
     *
     * @return array Returns an array of UserAccount objects
    */
    public function getAllUsers(): array
    {
        $db_conn = Database::getConnection();
        try {
            $sql = "SELECT * FROM `Users`";
            $stmt = $db_conn->prepare($sql);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_CLASS, 'UserAccount');
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Retrieves a User Account by ID
     *
     * @param int $id User ID
     * @return ?UserAccount Returns UserAccount object if found, null otherwise
    */
    public function getUserById(int $id): ?UserAccount
    {
        $db_conn = Database::getConnection();
        try {
            $sql = "SELECT * FROM `Users` WHERE `id` = :id";
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':id', $id);
            $stmt->execute();
            return $stmt->fetchObject('UserAccount') ?: null;
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return null;
        }
    }

    /**
     * Searches for User Accounts by username or email
     *
     * @param string $searchTerm Search term
     * @return array Returns an array of UserAccount objects
    */
    public function searchUsers(string $searchTerm): array
    {
        $db_conn = Database::getConnection();
        try {
            $sql = "SELECT * FROM `Users` WHERE `username` LIKE :searchTerm OR `email` LIKE :searchTerm";
            $stmt = $db_conn->prepare($sql);
            $likeTerm = '%' . $searchTerm . '%';
            $stmt->bindParam(':searchTerm', $likeTerm);
            $stmt->execute();
            return $stmt->fetchAll(PDO::FETCH_CLASS, 'UserAccount');
        } catch (PDOException $e) {
            error_log("Database query failed: " . $e->getMessage());
            return [];
        }
    }

    /**
     * Updates an existing User Account
     *
     * @param int $id User ID
     * @param string $username Username
     * @param string $email Email
     * @param int $isAdmin Is Admin (0 or 1)
     * @param int $isActive Is Active (0 or 1)
     * @return bool Returns true if update successful, false otherwise
    */
    public function updateUserAccount(int $id, string $username, string $email, ?string $password, int $isAdmin, int $isActive): bool
    {
        $db_conn = Database::getConnection();
        try {
            $sql = "UPDATE `Users`
                    SET `username` = :username, `email` = :email, `is_admin` = :isAdmin, `is_active` = :isActive";
            
            if ($password !== null && $password !== '') {
                $sql .= ", `password` = :password";
            }
            
            $sql .= " WHERE `id` = :id";
            
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':username', $username);
            $stmt->bindParam(':email', $email);
            $stmt->bindParam(':isAdmin', $isAdmin, PDO::PARAM_INT);
            $stmt->bindParam(':isActive', $isActive, PDO::PARAM_INT);
            if ($password !== null && $password !== '') {
                $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
                $stmt->bindParam(':password', $hashedPassword);
            }
            $stmt->bindParam(':id', $id, PDO::PARAM_INT);
            return $stmt->execute();
        } catch (PDOException $e) {
            error_log("Database update failed: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Deletes a User Account
     *
     * @param int $id User ID
     * @return bool Returns true if delete successful, false otherwise
    */
    public function deleteUserAccount(int $id): bool
    {
        $db_conn = Database::getConnection();
        try {
            $sql = "DELETE FROM `Users` WHERE `id` = :id";
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':id', $id, PDO::PARAM_INT);
            return $stmt->execute();
        } catch (PDOException $e) {
            error_log("Database delete failed: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Updates a User's Password
     *
     * @param int    $userID        User ID
     * @param string $oldPassword   Old Password
     * @param string $newPassword   New Password
     *
     * @return bool Returns true if Update Operation Success, Else false
    */
    public function updatePassword(int $userID, string $oldPassword, string $newPassword): int
    {
        $db_conn = Database::getConnection();

        try {
            // First, get the current user to verify the old password
            $sql = "SELECT * FROM `Users` WHERE `id` = :id";
            $stmt = $db_conn->prepare($sql);
            $stmt->bindParam(':id', $userID, PDO::PARAM_INT);
            $stmt->execute();

            if ($stmt->rowCount() == 1) {
                $userAccount = $stmt->fetchObject('UserAccount');
            } else {
                // User not found
                return -1;
            }

            // Verify the old password
            if (password_verify($oldPassword, $userAccount->getPassword())) {
                // Hash the new password
                $newPasswdHash = password_hash($newPassword, PASSWORD_DEFAULT);

                // Update the password in the database
                $updateSql = "UPDATE `Users` SET `password` = :password WHERE `id` = :id";
                $updateStmt = $db_conn->prepare($updateSql);
                $updateStmt->bindParam(':password', $newPasswdHash);
                $updateStmt->bindParam(':id', $userID, PDO::PARAM_INT);
                $execResult = $updateStmt->execute();

                if ($execResult) {
                    return 1;
                }
                else {
                    return -1;
                }
            } else {
                // Old password does not match
                error_log("Password update failed: Old password does not match for user ID " . $userID);
                return 0;
            }
        } catch (PDOException $e) {
            error_log("Database update failed: " . $e->getMessage());
            return -1;
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

    public function isAdmin(): int
    {
        return $this->is_admin;
    }
    
    public function isActive(): int
    {
        return $this->is_active;
    }
}