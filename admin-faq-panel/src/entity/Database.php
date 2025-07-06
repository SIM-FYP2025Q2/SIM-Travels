<?php

class Database
{
    private static $instance = null;
    private $pdo;

    private function __construct()
    {

        $environment = getenv('ENV');

        if ($environment == "PROD") {
            $host = getenv('DB_HOST');
            $port = getenv('DB_PORT');
            $db   = getenv('DB_NAME');
            $user = getenv('DB_USER');
            $pass = getenv('DB_PASS');
            $dsn = "mysql:host=$host;port=$port;dbname=$db;charset=utf8mb4";
        } else {
            $host = getenv('DB_HOST_STAGING');
            $port = getenv('DB_PORT_STAGING');
            $db   = getenv('DB_NAME_STAGING');
            $user = getenv('DB_USER_STAGING');
            $pass = getenv('DB_PASS_STAGING');
            $dsn = "mysql:host=$host;port=$port;dbname=$db;charset=utf8mb4";
        }

        try {
            $this->pdo = new PDO($dsn, $user, $pass);
        } catch (PDOException $e) {
            throw new PDOException($e->getMessage(), (int)$e->getCode());
        }
    }

    public static function getConnection()
    {
        if (self::$instance === null) {
            self::$instance = new Database();
        }
        return self::$instance->pdo;
    }
}