from pydantic import Field
from pydantic_settings import BaseSettings


class WebhookSettings(BaseSettings):
    lambda_run_id: str = Field(default="", env="LAMBDA_RUN_ID")
    xero_webhook_key: str = Field(..., env="XERO_WEBHOOK_KEY")
