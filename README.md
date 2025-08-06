# QRZ MCP Server

A minimal **Model Context Protocol** server built with **FastAPI** that forwards callsign lookup requests to the **QRZ.com XML lookup service**.

## Features

- `/lookup?callsign=XYZ` – Look up a callsign
- `/openapi.json` – OpenAPI schema served as YAML (MIME: `text/x-yaml`)

## Getting Started

1.  **Configure the application:**

    Copy the `.env.example` file to `.env` and edit it to add your QRZ.com username and password.

    ```bash
    cp .env.example .env
    # Now edit .env with your credentials
    ```

2.  **Run the application:**

    ```bash
    # Build & run with Docker Compose
    docker compose up --build

    # Or run locally (you need Python 3.11+)
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
