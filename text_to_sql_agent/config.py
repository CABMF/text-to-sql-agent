from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
   model_config = SettingsConfigDict(env_file=".env")
   database_url: str
   model_provider: Literal["mistral","anthropic"]="mistral"
   mistral_api_key : str | None =None
   antropic_api_key : str | None=None

