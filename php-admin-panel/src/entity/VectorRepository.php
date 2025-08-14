<?php

require("/var/www/html/vendor/autoload.php");

require_once("Database.php");
require_once("FaqRepository.php");
require_once("PineconeConn.php");

use Google\Auth\Credentials\ServiceAccountCredentials;

/**
 * Class VectorRepository
 *
 * Handles the generation of vector embeddings from Google Cloud's AI Platform
 * and upserting them into a Pinecone vector database. It also connects with 
 * MySQL Database for Sync, FAQ & Category Deletion Operations
 */
class VectorRepository
{
    /**
     * Authenticates with Google Cloud to obtain an access token.
     * @return ?string The access token on success, or null on failure.
     */
    private static function gcloud_auth(): ?string
    {

        $SERVICE_ACCOUNT_CREDENTIALS = base64_decode(getenv("SERVICE_ACCOUNT_CREDENTIALS"));
        $creds = json_decode($SERVICE_ACCOUNT_CREDENTIALS, true);

        $scopes = ['https://www.googleapis.com/auth/cloud-platform'];

        $creds = new ServiceAccountCredentials($scopes, $creds);
        $tokenArray = $creds->fetchAuthToken();

        return $tokenArray['access_token'] ?? null;
    }

    /**
     * Generates vector embeddings for a given question using Google's text-embedding model.
     *
     * Authenticates with Google Cloud, then sends a POST request to the
     * AI Platform API prediction endpoint with the question text. It returns the
     * resulting embedding values.
     * @param string $question The question text to be converted into a vector.
     * @return array An array of floating-point numbers representing the vector embedding, or an empty array on failure.
     */
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

    /**
     * Upserts unsynced FAQ records into the Pinecone vector database.
     *
     * Fetches records from the MySQL DB that are marked as not synced.
     * For each record, it generates a vector embedding for the question and then
     * upserts the vector along with its metadata (question, answer, category, link)
     * into Pinecone. If the upsert is successful, it updates the record's sync status
     * in the local database. A 2-second sleep is included between each upsert to avoid
     * rate-limiting issues.
     * 
     * @return bool Returns true if all records were synced successfully, false if any operation failed.
     */
    public function upsertVectors(): bool
    {
        $upsertStatus = true; // Default Return Flag

        // Connect to Pinecone
        $pinecone = PineconeConn::getConnection();

        // Fetch Unsynced Records
        $faqRepo = new FaqRepository();
        $unsyncedData = $faqRepo->fetchUnsyncedRecords();

        // No Records to Sync
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
            } else { // With Link Metadata
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

    /**
     * Delete FAQ Record from Pinecone Vector Database, then MySQL Database
     * @return bool Returns true record deleted successfully, false if any operation failed.
     */
    public function deleteVector(int $id, int $is_synced): bool
    {
        // FaqRepo Object
        $faqRepo = new FaqRepository();

        if ($is_synced === 1) {
            // Connect to Pinecone
            $pinecone = PineconeConn::getConnection();
            $response = $pinecone->data()->vectors()->delete(
                ids: [(string) $id]
            );

            // Delete from MySQL Database
            if($response->successful()) {
                return $faqRepo->deleteFaq($id);;
            } else {
                return false;
            }
        }

        return $faqRepo->deleteFaq($id);
    }

    /**
     * Deletes all records associated with a category from Pinecone Vector Database, then MySQL Database
     *
     * @param int $categoryId The ID of the category whose associated FAQ vectors are to be deleted.
     * @return bool Returns true if all associated vectors were deleted successfully, false otherwise.
     */
    public function deleteVectorsByCategory(int $categoryId): bool
    {
        $faqRepo = new FaqRepository();
        $categoryName = $faqRepo->getCategoryById($categoryId);

        if ($categoryName === "") {
            return false;
        } else {
            // Connect to Pinecone
            $pinecone = PineconeConn::getConnection();
            $response = $pinecone->data()->vectors()->delete(
                filter: ['category' => $categoryName ]
            );

            // Delete from MySQL Database
            if($response->successful()) {
                return $faqRepo->deleteCategory($categoryId);
            } else {
                return false;
            }
        }

        return $faqRepo->deleteCategory($categoryId);
    }
}