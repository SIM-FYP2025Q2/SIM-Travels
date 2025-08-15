# FastAPI Sunshine Conversations Webhook

This is a Python FastAPI server that acts as a webhook for Zendesk Sunshine Conversations. It receives messages from a Sunshine Conversations app, processes them, interacts with a backend AI agent, and sends replies back to the user.

## Environment Configuration

Before running the application, you need to create a `.env` file in the root of the project. You can copy the `.env.example` file to create it.

This file contains the following environment variables that need to be configured:

*   `ZENDESK_SUBDOMAIN`: Your Zendesk Subdomain.
*   `KEY_ID`: Your Sunshine Conversations API Key ID.
*   `KEY_SECRET`: Your Sunshine Conversations API Key Secret.

## Setup & Run the Application

To run the application, you need to have Python 3.11+ and `uv` installed on your system. You can find installation instructions for `uv` [here](https://github.com/astral-sh/uv).

1.  **Navigate to the project directory.**
    ```bash
    cd fastapi-sunshine-conversations
    ```

2.  **Create the virtual environment and install dependencies:**
    ```bash
    uv sync
    ```
    This command will create a virtual environment (if it doesn't exist) and install all the dependencies listed in `pyproject.toml`.

3.  **Run the server:**
    ```bash
    uv run fastapi run
    ```

## Webhook Configuration

Once the server is running, it will listen for POST requests at the `/messages` endpoint.

You need to configure this URL as a webhook in your Zendesk Sunshine Conversations app settings:
You should expose port 8000 on your firewall or network (e.g. through ngrok).

`http://<your-public-ip>:8000/messages`

## Credits

This project utilizes the official Zendesk Sunshine Conversations Python SDK. The API documentation and examples from their GitHub repository were used as a reference. You can find the repository [here](https://github.com/zendesk/sunshine-conversations-python/blob/master/docs/ConversationsApi.md).
