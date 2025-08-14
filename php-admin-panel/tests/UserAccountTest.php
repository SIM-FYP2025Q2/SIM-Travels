<?php

use PHPUnit\Framework\TestCase;

require_once '/var/www/html/entity/UserAccount.php';
require_once '/var/www/html/entity/Database.php';

// PHPUnit Testing for UserAccount
class UserAccountTest extends TestCase
{
    private $userAccount;
    private static $testUserId;
    private static $testUsername = 'phpunit_user';
    private static $testEmail = 'phpunit@example.com';
    private static $testPassword = 'password123';

    protected function setUp(): void
    {
        $this->userAccount = new UserAccount();
        
        $db_conn = Database::getConnection();
        $stmt = $db_conn->prepare("DELETE FROM Users WHERE email = :email OR username = :username");
        $stmt->execute(['email' => self::$testEmail, 'username' => self::$testUsername]);

        $result = $this->userAccount->createUserAccount(self::$testUsername, self::$testPassword, self::$testEmail);
        
        $stmt = $db_conn->prepare("SELECT id FROM Users WHERE email = :email");
        $stmt->execute(['email' => self::$testEmail]);
        self::$testUserId = $stmt->fetchColumn();
    }

    // Test 1: Successful login
    public function testLoginSuccess()
    {
        $user = $this->userAccount->login(self::$testEmail, self::$testPassword);
        $this->assertInstanceOf(UserAccount::class, $user);
        $this->assertEquals(self::$testUserId, $user->getId());
    }

    // Test 2: Failed login with wrong password
    public function testLoginFail()
    {
        $user = $this->userAccount->login(self::$testEmail, 'wrongpassword');
        $this->assertNull($user);
    }

    // Test 3: Creating a user with an existing email
    public function testCreateDuplicateUser()
    {
        $result = $this->userAccount->createUserAccount('anotheruser', 'password123', self::$testEmail);
        $this->assertFalse($result);
    }

    // Test 4: View a specific user account
    public function testGetUserById()
    {
        $user = $this->userAccount->getUserById(self::$testUserId);
        $this->assertInstanceOf(UserAccount::class, $user);
        $this->assertEquals(self::$testUsername, $user->getUsername());
    }

    // Test 5: View all user accounts
    public function testGetAllUsers()
    {
        $users = $this->userAccount->getAllUsers();
        $this->assertIsArray($users);
        
        $found = false;
        foreach ($users as $user) {
            if ($user->getId() == self::$testUserId) {
                $found = true;
                break;
            }
        }
        $this->assertTrue($found, "Test user not found in all users list.");
    }

    // Test 6: Search for a user
    public function testSearchUsers()
    {
        $users = $this->userAccount->searchUsers('phpunit');
        $this->assertIsArray($users);
        $this->assertNotEmpty($users);
        $this->assertEquals(self::$testUserId, $users[0]->getId());
    }

    // Test 7: Update a user\'s account details
    public function testUpdateUserAccount()
    {
        $newUsername = 'phpunit_user_updated';
        $status = $this->userAccount->updateUserAccount(self::$testUserId, $newUsername, self::$testEmail, null, 0, 1);
        $this->assertTrue($status);

        $updatedUser = $this->userAccount->getUserById(self::$testUserId);
        $this->assertEquals($newUsername, $updatedUser->getUsername());
        
        self::$testUsername = $newUsername;
    }

    // Test 8: Update a user\'s password
    public function testUpdatePassword()
    {
        $newPassword = 'newpassword123';
        $result = $this->userAccount->updatePassword(self::$testUserId, self::$testPassword, $newPassword);
        $this->assertEquals(1, $result, "Password update should be successful.");

        $user = $this->userAccount->login(self::$testEmail, $newPassword);
        $this->assertInstanceOf(UserAccount::class, $user);

        self::$testPassword = $newPassword;
    }

    protected function tearDown(): void
    {
        $this->userAccount->deleteUserAccount(self::$testUserId);
    }
}
