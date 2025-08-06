from __future__ import annotations

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.openapi.utils import get_openapi

from config import settings
from qrz import lookup_callsign
from schemas import QRZLookupResponse
import httpx

# Initialize the FastAPI application
app = FastAPI(
    title="QRZ MCP Server",
    description="MCP server that exposes QRZ.com XML lookup.",
    version="1.0.0",
    openapi_url=None,  # Disable the default /openapi.json to provide our own
)

def get_openapi_schema():
    """
    Generates and caches the OpenAPI schema for the application.
    This allows us to serve the schema in both JSON and YAML formats.
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    """Serves the OpenAPI schema in JSON format."""
    return JSONResponse(get_openapi_schema())


@app.get("/openapi.yaml", include_in_schema=False)
async def get_open_api_yaml():
    """Serves the OpenAPI schema in YAML format."""
    openapi_schema = get_openapi_schema()
    yaml_schema = yaml.dump(openapi_schema)
    return PlainTextResponse(yaml_schema, media_type="text/x-yaml")



# --------------------------------------------------------------------------- #
# QRZ lookup endpoint
# --------------------------------------------------------------------------- #
@app.get("/lookup", response_model=QRZLookupResponse)
async def lookup(callsign: str = Query(..., min_length=3, max_length=10)):
    """
    Look up a callsign via the QRZ.com XML service.

    This endpoint takes a callsign as a query parameter, queries the QRZ.com
    XML API, and returns the parsed data in a structured JSON format.
    """
    try:
        # Perform the lookup and extract the relevant part of the response
        raw = await lookup_callsign(callsign.upper())
        data = raw.get("QRZDatabase", {}).get("Callsign")
        if not data:
            raise ValueError("Callsign not found or invalid response from QRZ service.")
    except httpx.HTTPError as exc:
        # Handle errors from the QRZ service (e.g., network issues, 5xx errors)
        raise HTTPException(status_code=502, detail="QRZ service unavailable") from exc
    except ValueError as exc:
        # Handle cases where the callsign is not found or the response is malformed
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    # If successful, return the data, which will be validated against the QRZLookupResponse model
    return QRZLookupResponse(**data)
