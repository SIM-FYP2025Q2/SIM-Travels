# SIM Travels MySQL+Pinecone FAQ Panel

This is a PHP-based admin panel for managing a knowledge base system. It allows users to perform CRUD operations on FAQs and categories stored in a MySQL database. The application also integrates with Pinecone's vector database, generating vector embeddings for the FAQs using Google Cloud's AI Platform and keeping the Pinecone index synchronized with the MySQL database.

## Project Structure
The repository is organized as follows:
```
admin-faq-panel/
├── src/            Boundary, Controller and Entity Files
├── tests/          Test Scripts to Insert Tests Data / Test Functions (phpunit)
├── Dockerfile      Contains instructions for building the Docker image for the application
├── README.Docker.md This file
├── .dockerignore   Files and directories to exclude when building Docker images
├── compose.yaml    Defines application services for Docker Compose
├── composer.json   Defines PHP Dependencies (phpunit, pinecone-php, google/auth)
```

## Environment Configuration

Before running the application, you need to create a `.env` file in the root of the project. You can copy the `.env.example` file to create it.

This file contains the following environment variables that need to be configured:

*   `ENV`: Set to `PROD` for production or `STAGING` for development.
*   `SERVICE_ACCOUNT_CREDENTIALS`: Base64 encoded string for Google Service Account.
*   `PROJECT_ID`: Your Google Cloud Project ID.
*   `DB_HOST`: Production database host.
*   `DB_PORT`: Port for the production database (default: 3306).
*   `DB_NAME`: Production database name.
*   `DB_USER`: Username for the production database.
*   `DB_PASS`: Password for the production database.
*   `DB_HOST_STAGING`: Staging database host (e.g., `host.docker.internal`).
*   `DB_PORT_STAGING`: Port for the staging database (default: 3306).
*   `DB_NAME_STAGING`: Staging database name.
*   `DB_USER_STAGING`: Username for the staging database.
*   `DB_PASS_STAGING`: Password for the staging database.
*   `PINECONE_INDEX_HOST`: Your Pinecone index host.
*   `PINECONE_API_KEY`: Your Pinecone API key.

## Setup & Run the Application

To run the application, you need to have Docker and Docker Compose installed on your system. You can find installation instructions for Docker [here](https://docs.docker.com/get-started/get-docker/).

1.  **Navigate to the project directory.**
    ```bash
    cd admin-faq-panel
    ```

2.  **Starting the Application using Docker Compose:**
    ```bash
    docker compose up --build
    ```
    This command will build the Docker image (if necessary) and start the container defined in the `compose.yaml` file.

3.  **Accessing the Application:**

    Once the container is running, you can access the application through the following URL in your web browser:
    * **Login Page:** [`http://localhost:9000`](http://localhost:9000)

4.  **Stopping the Application:**

    To stop the running container, use the following command in the project directory:
    ```bash
    docker compose down
    ```

**Running PHPUnit Tests:**

Use the `docker-compose exec` command to run the PHP script within the PHP application container.

```bash
# PHPUnit Test Scripts
docker-compose exec server php ./vendor/bin/phpunit tests/
```

You will see output in your terminal successful/fail assertions.

---