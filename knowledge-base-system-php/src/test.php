<?php

require 'vendor/autoload.php';

use Google\Auth\Credentials\ServiceAccountCredentials;

function gcloud_auth(): ?string
{

    $SERVICE_ACCOUNT_CREDENTIALS = base64_decode(getenv("SERVICE_ACCOUNT_CREDENTIALS"));
    $creds = json_decode($SERVICE_ACCOUNT_CREDENTIALS, true);

    $scopes = ['https://www.googleapis.com/auth/cloud-platform'];

    $creds = new ServiceAccountCredentials($scopes, $creds);
    $tokenArray = $creds->fetchAuthToken();

    return $tokenArray['access_token'] ?? null;
}

$token = gcloud_auth();

$headers = [
    "Authorization: Bearer " . $token,
    "Content-Type: application/json; charset=utf-8"
];

$ch = curl_init();

$data = [
    "instances" => [
        [
            "task_type" => "QUESTION_ANSWERING",
            "content" => "What the baggage policy for AirAsia?"
        ]
    ],
    "parameters" => [
        "outputDimensionality" => 768
    ]
];

$jsonData = json_encode($data);

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

$response = curl_exec($ch);

// Check for cURL errors
if (curl_errno($ch)) {
    echo 'cURL error: ' . curl_error($ch);
}

curl_close($ch);

// Process the API response
if ($response) {
   $data = json_decode($response, true);
   $embeddingValues = $data['predictions'][0]['embeddings']['values'];

    // Example: output first 5 values
    foreach (array_slice($embeddingValues, 0, 5) as $i => $value) {
        echo "[$i] = $value\n";
    }
} else {
    echo "No response received.";
}