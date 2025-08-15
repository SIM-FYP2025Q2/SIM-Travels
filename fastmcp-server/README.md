# FastMCP Amadeus Travel Assistant Server

This is a Python FastMCP server that provides a set of tools for searching flights, hotels, and airport transfers using the Amadeus API. It uses FastMCP to expose these tools as a web service.

## Environment Configuration

Before running the application, you need to create a `.env` file in the root of the project. You can copy the `.env.example` file to create it.

This file contains the following environment variables that need to be configured:

*   `API_KEY`: Your Amadeus API Key.
*   `API_SECRET`: Your Amadeus API Secret.
*   `GEOLOCATION_API_KEY`: Your Google Geocoding API Key.

## Setup & Run the Application

To run the application, you need to have Python 3.11+ and `uv` installed on your system. You can find installation instructions for `uv` [here](https://github.com/astral-sh/uv).

1.  **Navigate to the project directory.**
    ```bash
    cd fastmcp-server
    ```

2.  **Create the virtual environment and install dependencies:**
    ```bash
    uv sync
    ```
    This command will create a virtual environment (if it doesn't exist) and install all the dependencies listed in `pyproject.toml`.

3.  **Run the server:**
    ```bash
    uv run python server.py
    ```

4.  **Accessing the Application:**

    Once the server is running, you can access the API at `http://localhost:7000`.