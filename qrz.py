"""
Utility module to talk to the QRZ.com XML lookup service.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Dict

import httpx
import xmltodict

from config import settings

async def lookup_callsign(callsign: str) -> dict:
    """
    Perform a GET request to the QRZ.com XML API and return the result as a dict.

    This function constructs the request with credentials from the application
    settings, sends it to the QRZ API, and handles the XML response.

    Args:
        callsign: The amateur radio callsign to look up.

    Returns:
        A dictionary containing the parsed XML data from the QRZ API.

    Raises:
        httpx.HTTPError: If the request to the QRZ API fails (e.g., network
                         error, 4xx/5xx status code, or empty response body).
    """
    # Parameters for the QRZ API call, including credentials
    params = {
        "username": settings.qrz_user,
        "password": settings.qrz_pass.get_secret_value(),
        "callsign": callsign
    }

    async with httpx.AsyncClient() as client:
        # Make the asynchronous GET request
        resp = await client.get(settings.qrz_base_url, params=params)
        # Raise an exception for non-2xx status codes
        resp.raise_for_status()

        # Convert the XML response to a dict
        xml_text = resp.text
        if not xml_text.strip():  # Defensive check for an empty response body
            raise httpx.HTTPError("Empty response body from QRZ")

        # xmltodict parses XML into an OrderedDict; we convert it to a standard dict
        # for easier processing downstream.
        parsed = xmltodict.parse(xml_text)
        return dict(parsed)
