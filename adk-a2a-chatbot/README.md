# SIM Travels - Amadeus Travel Assistant

This is a Python-based travel assistant chatbot that provides a set of tools for searching flights, hotels, and airport transfers using the Amadeus API. It is built using the Google Agent Development Kit (ADK) and exposes its services through a chat interface.

## Architecture

The application consists of two main components:

*   **Customer Support Agent (`customer_support_agent`):** This is the main, user-facing agent. It acts as a router, understanding the user's request and delegating it to the appropriate specialized sub-agent.
*   **Remote A2A Agents (`remote_a2a`):** These are specialized, backend agents that handle specific tasks like searching for flight, hotel, or transfer offers. They are exposed as a web service using the ADK A2A server.

## Environment Configuration

Before running the application, you need to create a `.env` file in the root of the project. This file should contain the following environment variables:

*   `MCP_SERVER_URL`: The URL of the FastMCP server that connects to the Amadeus API.
*   `PINECONE_API_KEY`: Your Pinecone API Key for the RAG search functionality.
*   `PINECONE_INDEX_HOST`: Your Pinecone index host.
*   `ZENDESK_API_URL`: The API URL for your Zendesk instance.
*   `ZENDESK_EMAIL`: The email associated with your Zendesk account.
*   `ZENDESK_API_KEY`: Your Zendesk API key.
*   `MYSQL_USER`: The username for your MySQL database.
*   `MYSQL_PASSWD`: The password for your MySQL database.
*   `MYSQL_SERVER_URL`: The URL of your MySQL server.
*   `TAVILY_API_KEY`: Your Tavily API key for search functionalities.

## Setup & Run the Application

To run the application, you need to have Python 3.11+ and `uv` installed on your system. You can find installation instructions for `uv` [here](https://github.com/astral-sh/uv).

1.  **Navigate to the project directory.**
    ```bash
    cd adk-a2a-chatbot
    ```

2.  **Create the virtual environment and install dependencies:**
    ```bash
    uv sync
    ```
    This command will create a virtual environment (if it doesn't exist) and install all the dependencies listed in `pyproject.toml`.

3.  **Run the Remote A2A Agents:**
    Open a terminal and run the following command to start the server for the remote agents:
    ```bash
    uv run adk api_server --a2a --port 8001 remote_a2a
    ```

4.  **Run the Customer Support Agent:**
    Open a second terminal and run the main application:
    ```bash
    uv run main.py
    ```

5.  **Accessing the Application:**
    Once the application is running, you can interact with the chatbot through its interface. The host and port will be displayed in the console when you run `main.py`.

## Acknowledgements

Much of the tutorial and sample code was referred from the official ADK documentation: https://google.github.io/adk-docs/
