# adk-chatbot

This is a chatbot application built with the Google ADK.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.11 or greater
* `uv` or `pip` for package management

### Setup (uv)

1. **Create a virtual environment:**

    ```bash
    uv venv
    ```

2. **Activate the virtual environment:**
    * On Windows:

        ```bash
        .venv\Scripts\activate
        ```

    * On macOS/Linux:

        ```bash
        source .venv/bin/activate
        ```

3. **Install dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

### Setup (pip)

1. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment:**
    * On Windows:

        ```bash
        .venv\Scripts\activate
        ```

    * On macOS/Linux:

        ```bash
        source .venv/bin/activate
        ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` file** in the root directory by copying the `.env.example` file:

    ```bash
    cp .env.example .env
    ```

2. **Update the `.env` file** with your specific configurations, such as API keys and project IDs.

3. **Repeat the process for each agent's `.env` file:**
    * For `customer_support_agent`:

        ```bash
        cp customer_support_agent/.env.example customer_support_agent/.env
        ```

    * For `flight_offers_agent`:

        ```bash
        cp flight_offers_agent/.env.example flight_offers_agent/.env
        ```

    * Update these new `.env` files with the necessary credentials.

## Running the Application

Once the setup and configuration are complete, you can run the agent development with the following command:

```bash
./adk-chatbot > adk-web
```

This will start the FastAPI server, and you can access the chatbot at `http://localhost:8080`.
