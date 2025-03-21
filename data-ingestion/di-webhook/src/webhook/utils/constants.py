from pydantic import Field
from pydantic_settings import BaseSettings


class WebhookSettings(BaseSettings):
    xero_webhook_key: str = Field(..., env="XERO_WEBHOOK_KEY")
