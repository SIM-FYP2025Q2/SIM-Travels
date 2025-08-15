# Project Setup Guide

This README.me will guide you through setting up SIM TRAVELS Website, setup using **React + Vite** for frontend, and **Node.js + Express + MySQL** for backend.

---

## 1. Create a New Vite Project

1. Open your terminal in VS Code.
2. Run:
   ```bash
   npm create vite@latest
3. **If you get an error** saying scripts are disabled, run:

    ```bash
    Set-ExecutionPolicy -ExecutionPolicy Undefined -Scope CurrentUser
    ```

4. Then try again:

    ```bash
    npm create vite@latest
    5. Follow the prompts:
    -   **Project name**: (your choice)
    -   **Package name**: (press Enter to use default)
        -   **Framework**: React
        -   **Variant**: JavaScript
    ---

## 2. Install Dependencies

1. Move into your new project folder:

    ```bash
    cd your--project--name
    2. Install required packages:
    ```

- **Frontend**:

    ```bash
    npm install
    npm install react-router-dom
    npm install bootstrap
    npm install react-bootstrap bootstrap
    npm install axios
    ```

3. Install required packages:

- **Backend:**

    ```bash
    npm install express mysql2 cors dotenv
    npm install express-session
    ```

**Dependency Notes:**
 -   **react-router-dom** – Page routing for SPA.
 -   **bootstrap** – CSS framework.
 -   **react-bootstrap** – Bootstrap components for React.
 -   **express** – Backend server framework.
 -   **mysql2** – MySQL driver for Node.js.
 -   **cors** – Enables frontend-backend communication.
 -   **dotenv** – Environment variables (e.g., DB credentials).
 -   **axios** – HTTP requests from frontend to backend.
 -   **express-session** – Session handling for login/logout.

---

## 3. Recommended Extensions

Install **React ES7+ Snippets** in VS Code for quick React component shortcuts (e.g., `rafce`).

---
## 4. Running the Project

Before you run the project add your Zendesk Widget Snippet in `index.html`

```bash
    ...
    <!-- Start of Zendesk Widget script -->
    <script id="ze-snippet" src="..."> </script>
    <!-- End of  Zendesk Widget script -->
    ...
```

Open **two terminal windows** in VS Code:

1. **Frontend (Vite Dev Server)**:

    ```bash
    npm run dev
    ```

2. **Backend (Express Server)**:

    ```bash
    node server.js
    ```

3. **To access the site locally**:

    ```bash
    http://localhost:xxxx
    ```
    (Replace **xxxx** with port shown in Vite terminal.)


---
## 5. Full Rebuild (Clear Cache)

1. If you need a clean rebuild:

    ```bash
    rm -rf node_modules dist.vite
    npm install
    npm run dev
    ```
