"""
Utility module to talk to QRZ.com XML lookup service.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Dict

import httpx
import xmltodict

from config import settings

async def lookup_callsign(callsign: str) -> dict:
    """
    Perform a GET request to the QRZ API and return the result as a dict.

    The QRZ API returns XML; we convert it to a Python dict with
    `xmltodict.parse`.  The top‑level key is 'xmldata', which contains
    the actual call‑sign information under 'call'.
    """
    params ={"username": settings.qrz_user, "password": settings.qrz_pass.get_secret_value(), "callsign": callsign}
    async with httpx.AsyncClient() as client:
        resp = await client.get(settings.qrz_base_url, params=params)
        resp.raise_for_status()          # raise for 4xx/5xx

        # Convert the XML response to a dict
        xml_text = resp.text
        if not xml_text.strip():         # defensive: empty body
            raise httpx.HTTPError("Empty response body from QRZ")

        # xmltodict returns an OrderedDict; turn it into a normal dict
        parsed = xmltodict.parse(xml_text)
        return dict(parsed)
