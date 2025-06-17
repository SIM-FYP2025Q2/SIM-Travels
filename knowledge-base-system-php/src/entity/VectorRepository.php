<?php

require("/var/www/html/vendor/autoload.php");

require_once("Database.php");
require_once("FaqRepository.php");

use Google\Auth\Credentials\ServiceAccountCredentials;
use \Probots\Pinecone\Client as Pinecone;


class VectorRepository
{
    private static function gcloud_auth(): ?string
    {

        $SERVICE_ACCOUNT_CREDENTIALS = base64_decode(getenv("SERVICE_ACCOUNT_CREDENTIALS"));
        $creds = json_decode($SERVICE_ACCOUNT_CREDENTIALS, true);

        $scopes = ['https://www.googleapis.com/auth/cloud-platform'];

        $creds = new ServiceAccountCredentials($scopes, $creds);
        $tokenArray = $creds->fetchAuthToken();

        return $tokenArray['access_token'] ?? null;
    }

    private static function generateVectors(string $question): array
    {
        $token = self::gcloud_auth();

        if (is_null($token)) {
            return [];
        }

        // Prepare cURL Header
        $ch = curl_init();
        $headers = [
            "Authorization: Bearer " . $token,
            "Content-Type: application/json; charset=utf-8"
        ];

        // JSON Encode Data
        $data = [
            "instances" => [
                [
                    "task_type" => "QUESTION_ANSWERING",
                    "content" => $question
                ]
            ],
            "parameters" => [
                "outputDimensionality" => 768
            ]
        ];
        $jsonData = json_encode($data);

        // Set cURL Options Array
        curl_setopt_array($ch, [
            CURLOPT_CUSTOMREQUEST => "POST",
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POSTFIELDS => $jsonData,
            CURLOPT_URL =>  "https://us-central1-aiplatform.googleapis.com/v1/projects/" .
                            getenv('PROJECT_ID') .
                            "/locations/us-central1/publishers/google" .
                            "/models/text-embedding-005:predict"
        ]);
        

        // POST Request
        $response = curl_exec($ch);

        // Check for cURL errors
        if (curl_errno($ch)) {
            return [];
        }
        curl_close($ch); // Close cURL Connection

        // Process Response
        if ($response) {
            $data = json_decode($response, true);
            $embeddingVals = $data['predictions'][0]['embeddings']['values'];
            return $embeddingVals;
        } else {
            return [];
        }
    }

    public function upsertVectors(): bool
    {
        $upsertStatus = true;
        $api_key = getenv("PINECONE_API_KEY");
        $index = getenv("PINECONE_INDEX_HOST");
        $pinecone = new Pinecone($api_key, $index);
        
        $faqRepo = new FaqRepository();
        $unsyncedData = $faqRepo->fetchUnsyncedRecords();

        if (empty($unsyncedData)) {
            return $upsertStatus;
        }

        foreach ($unsyncedData as $data) {

            // Generate Vector Embeddings
            $vectorArr = self::generateVectors($data['question']);
            
            // Do not upsert if vector array is empty
            if (empty($vectorArr)) {
                $upsertStatus = false;
                continue;
            }
            
            // Upsert Vectors (with/without Link Metadata)
            if (is_null($data['link'])) {
                $response = $pinecone->data()->vectors()->upsert(vectors: [
                    'id' => (string) $data['id'],
                    'values' => $vectorArr,
                    'metadata' => [
                        'question' => $data['question'],
                        'answer' => $data['answer'],
                        'category' => $data['category']
                    ]
                ]);
            } else {
                $response = $pinecone->data()->vectors()->upsert(vectors: [
                    'id' => (string) $data['id'],
                    'values' => $vectorArr,
                    'metadata' => [
                        'question' => $data['question'],
                        'answer' => $data['answer'],
                        'category' => $data['category'],
                        'link' => $data['link']
                    ]
                ]);
            }

            // Update MySQL for Successful Updates
            if($response->successful()) {
                $id = (int) $data['id'];
                $faqRepo->setSyncStatus($id, 1);
            } else {
                $upsertStatus = false;
            }

            sleep(2); // Wait before Next Update
        }
        return $upsertStatus;
    }
}