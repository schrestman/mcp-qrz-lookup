"""
Pydantic models for API payloads and responses.
"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field

class QRZLookupResponse(BaseModel):
    """
    Representation of the relevant QRZ XML fields we care about.
    """

    call: str = Field(..., description="The queried callsign")
    fname: Optional[str] = Field(None, description="First name of the license holder")
    name: Optional[str] = Field(None, description="Last name of the license holder")
    addr1: Optional[str] = Field(None, description="Address of license holder")
    addr2: Optional[str] = Field(None, description="City of the license holder")
    state: Optional[str] = Field(None, description="State/province")
    zip: Optional[str] = Field(None, description="Zip code of the license holder")
    country: Optional[str] = Field(None, description="Country")
    license_class: Optional[str] = Field(alias="class", description="License Class")


