from __future__ import annotations

import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.openapi.utils import get_openapi

from config import settings
from qrz import lookup_callsign
from schemas import QRZLookupResponse
import httpx

app = FastAPI(
    title="QRZ MCP Server",
    description="MCP server that exposes QRZ.com XML lookup.",
    version="1.0.0",
    openapi_url=None,  # Disable the default /openapi.json
)

def get_openapi_schema():
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
    return JSONResponse(get_openapi_schema())


@app.get("/openapi.yaml", include_in_schema=False)
async def get_open_api_yaml():
    openapi_schema = get_openapi_schema()
    yaml_schema = yaml.dump(openapi_schema)
    return PlainTextResponse(yaml_schema, media_type="text/x-yaml")



# --------------------------------------------------------------------------- #
# QRZ lookup endpoint
# --------------------------------------------------------------------------- #
@app.get("/lookup", response_model=QRZLookupResponse)
async def lookup(callsign: str = Query(..., min_length=3, max_length=10)):
    """
    Look up a callsign via QRZ.com XML service.
    """
    try:
        raw = await lookup_callsign(callsign.upper())
        data = raw.get("QRZDatabase", {}).get("Callsign")
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="QRZ service unavailable") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return QRZLookupResponse(**data)
