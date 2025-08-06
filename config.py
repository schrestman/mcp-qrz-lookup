# config.py
from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

class Settings(BaseSettings):
    # --- General FastAPI stuff --------------------------------------------
    host: str = Field("0.0.0.0")
    port: int = Field(8000)

    # --- QRZ‑specific configuration ---------------------------------------
    qrz_base_url: str = Field(
        ...,
        env="QRZ_BASE_URL",
        description="Base URL for the QRZ API",
    )
    qrz_user: str = Field(
        ...,
        env="QRZ_USER",
        description="Your QRZ username"
    )
    qrz_pass: SecretStr = Field(
            ...,
            env="QRZ_PASS",
            description="Your QRZ password"
    )

    # Tell pydantic‑settings to look for a .env file by default
    model_config = {"env_file": ".env", "extra": "ignore"}

# Instantiate a *single* global configuration object
settings = Settings()
