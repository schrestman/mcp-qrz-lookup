# QRZ MCP Server

This project provides a simple, containerized FastAPI application that acts as a proxy to the QRZ.com XML data service. It exposes a single RESTful API endpoint to look up amateur radio callsigns and returns the data in a clean JSON format.

The application is designed to be a "Model Context Protocol" (MCP) server, providing a stable and well-defined interface to the QRZ.com service.

## Features

*   **Simple REST API**: A single `/lookup` endpoint for all callsign queries.
*   **Structured JSON Response**: Converts the QRZ.com XML data to a predictable JSON object.
*   **OpenAPI Documentation**: Automatically generated and available at `/openapi.json` and `/openapi.yaml`.
*   **Containerized**: Includes a `Dockerfile` and `docker-compose.yml` for easy deployment.
*   **Configuration Management**: Uses Pydantic for robust settings management from environment variables or a `.env` file.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)
*   A QRZ.com account with XML data access.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/schrestman/mcp-qrz-lookup.git
    cd mcp-qrz-lookup
    ```

2.  **Create a `.env` file:**

    Copy the example environment file and fill in your QRZ.com credentials and the API URL.

    ```bash
    cp .env.example .env
    ```

    Your `.env` file should look like this:

    ```ini
    # .env
    QRZ_BASE_URL=https://xmldata.qrz.com/xml/current/
    QRZ_USER=your_qrz_username
    QRZ_PASS=your_qrz_password
    ```

3.  **Build and run the container:**

    ```bash
    docker-compose up --build
    ```

    The server will be running and accessible at `http://localhost:8000`.

## API Usage

The primary endpoint for interacting with the service is `/lookup`.

### `GET /lookup`

Looks up a given amateur radio callsign.

*   **Query Parameter:**
    *   `callsign` (string, required): The callsign to look up (e.g., "W1AW").
*   **Success Response (200 OK):**

    Returns a JSON object with the callsign information.

    ```json
    {
      "call": "W1AW",
      "fname": "ARRL HQ",
      "name": "ARRL",
      "addr1": "225 Main St",
      "addr2": "Newington",
      "state": "CT",
      "zip": "06111",
      "country": "United States",
      "license_class": "C"
    }
    ```

*   **Error Responses:**
    *   `422 Unprocessable Entity`: If the callsign is not found or the data from QRZ.com is invalid.
    *   `502 Bad Gateway`: If the service cannot connect to the QRZ.com API.

### Example Request

You can use `curl` or any HTTP client to make a request:

```bash
curl "http://localhost:8000/lookup?callsign=W1AW"
```

## API Documentation

The OpenAPI (Swagger) documentation is automatically generated and can be accessed at the following endpoints:

*   **JSON format**: `http://localhost:8000/openapi.json`
*   **YAML format**: `http://localhost:8000/openapi.yaml`

You can use these with tools like Swagger UI or Postman to explore the API.

## Project Structure

```
.
├── .env.example      # Example environment variables
├── .gitignore        # Files to ignore in git
├── config.py         # Pydantic configuration settings
├── docker-compose.yml# Docker Compose configuration
├── Dockerfile        # Docker build instructions
├── main.py           # FastAPI application and endpoints
├── qrz.py            # QRZ.com API interaction logic
├── README.md         # This file
├── requirements.txt  # Python dependencies
└── schemas.py        # Pydantic data models for API
```

## How It Works

1.  **`main.py`**: This file sets up the FastAPI application and defines the `/lookup` endpoint. When a request is received, it calls the `lookup_callsign` function.
2.  **`qrz.py`**: This module contains the `lookup_callsign` function, which is responsible for making the actual HTTP request to the QRZ.com XML API. It uses the `httpx` library for asynchronous requests.
3.  **`config.py`**: This file defines the `Settings` class using Pydantic, which loads configuration from environment variables (or a `.env` file). This is where the QRZ username, password, and API URL are managed.
4.  **`schemas.py`**: This file defines the `QRZLookupResponse` Pydantic model, which ensures that the data returned by the API is in a consistent and validated format.
5.  **`Dockerfile`**: This file contains the instructions to build a Docker image for the application, installing dependencies and running the Uvicorn server.
6.  **`docker-compose.yml`**: This file makes it easy to run the application and manage its lifecycle with a single command.
