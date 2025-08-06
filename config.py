# config.py
"""
This module defines the application's configuration using Pydantic's BaseSettings.
It allows for loading configuration from environment variables and a .env file,
making it easy to manage settings for different environments.
"""
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    """
    Defines the application's configuration settings.
    Pydantic automatically reads environment variables or values from a .env file.
    """
    # --- General FastAPI stuff --------------------------------------------
    host: str = Field("0.0.0.0", description="The host to bind the FastAPI server to.")
    port: int = Field(8000, description="The port to run the FastAPI server on.")

    # --- QRZ‑specific configuration ---------------------------------------
    qrz_base_url: str = Field(
        ...,
        env="QRZ_BASE_URL",
        description="Base URL for the QRZ XML API. This is a required setting.",
    )
    qrz_user: str = Field(
        ...,
        env="QRZ_USER",
        description="Your QRZ.com username. This is a required setting."
    )
    qrz_pass: SecretStr = Field(
            ...,
            env="QRZ_PASS",
            description="Your QRZ.com password. This is a required setting. `SecretStr` ensures the password is not exposed in logs or tracebacks."
    )

    # Tell pydantic‑settings to look for a .env file by default
    model_config = {"env_file": ".env", "extra": "ignore"}

# Instantiate a *single* global configuration object that can be imported elsewhere.
settings = Settings()
