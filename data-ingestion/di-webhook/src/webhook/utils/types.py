from pydantic import BaseModel


class WebhookEventMapping(BaseModel):
    datalake_domain: str
    event_name: str
