from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from webhook.routes import XeroRouter
from utils.constants import WebhookSettings

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()
settings = WebhookSettings()

log_event: bool = settings.lambda_run_id != ""

# Add routes here
app.include_router(XeroRouter, prefix="xero")


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP, log_event=log_event)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    app.append_context(api_settings=settings)
    return app.resolve(event, context)
