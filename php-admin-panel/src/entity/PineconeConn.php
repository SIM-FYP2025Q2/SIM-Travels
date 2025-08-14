<?php

require("/var/www/html/vendor/autoload.php");

use \Probots\Pinecone\Client as Pinecone;

class PineconeConn
{
    private static $instance = null;
    private $pinecone;

    private function __construct()
    {
        $index = getenv("PINECONE_INDEX_HOST");
        $api_key = getenv("PINECONE_API_KEY");

        try {
            $this->pinecone = new Pinecone($api_key, $index);
        } catch (Exception $e) {
            throw new Exception($e->getMessage());
        }
    }

    public static function getConnection()
    {
        if (self::$instance === null) {
            self::$instance = new PineconeConn();
        }
        return self::$instance->pinecone;
    }
}