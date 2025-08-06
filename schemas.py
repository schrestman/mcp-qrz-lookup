"""
Pydantic models for API payloads and responses.

This module defines the data structures used for validating and serializing
the data returned by the API. Using Pydantic models ensures that the API
responses are consistent and well-defined.
"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

class QRZLookupResponse(BaseModel):
    """
    A Pydantic model representing the relevant fields from the QRZ.com XML data.

    This model is used as the `response_model` in the FastAPI endpoint, which
    means FastAPI will automatically handle the validation and serialization
 of the outgoing data to match this structure. It also generates the
    corresponding schema in the OpenAPI documentation.
    """

    call: str = Field(..., description="The queried callsign")
    fname: Optional[str] = Field(None, description="First name of the license holder")
    name: Optional[str] = Field(None, description="Last name of the license holder")
    addr1: Optional[str] = Field(None, description="Street address of the license holder")
    addr2: Optional[str] = Field(None, description="City of the license holder")
    state: Optional[str] = Field(None, description="State or province of the license holder")
    zip: Optional[str] = Field(None, description="Zip or postal code of the license holder")
    country: Optional[str] = Field(None, description="Country of the license holder")
    # The `alias` is used because 'class' is a reserved keyword in Python.
    # Pydantic will map the 'class' field from the incoming data to this `license_class` attribute.
    license_class: Optional[str] = Field(alias="class", description="The operator's license class")


