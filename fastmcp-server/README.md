# FastMCP 2.0 Server

This document provides instructions on how to set up and run the FastMCP 2.0 server using either `uv` or `pip` for dependency management.

## Prerequisites

- Python 3.11 or higher
- `uv` (optional, for `uv` setup)
- `pip` (included with Python)

## Setup with `uv`

1. **Create a virtual environment:**

    ```bash
    uv venv
    ```

2. **Activate the virtual environment:**
    - On Windows:

      ```bash
      .venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source .venv/bin/activate
      ```

3. **Install dependencies:**

    ```bash
    uv pip install -r requirements.txt
    ```

## Setup with `pip`

1. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

2. **Activate the virtual environment:**
    - On Windows:

      ```bash
      .venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source .venv/bin/activate
      ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

The server requires certain environment variables to be set.

1. **Create a `.env` file** by copying the example file:

    ```bash
    cp .env.example .env
    ```

2. **Update the `.env` file** with your specific configuration details.

## Running the Server

Once the setup is complete and the environment variables are configured, you can run the server using `uv` or `python`.

```bash
uv run main.py
```

```python
python main.py
```

The server will be accessible at `http://127.0.0.1:7000/mcp`.
