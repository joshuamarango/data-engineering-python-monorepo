import hmac
import hashlib
import base64
import json

from http import HTTPStatus
from typing import Dict, Tuple

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import Response, content_types
from aws_lambda_powertools.event_handler.router import APIGatewayRouter

from webhook.utils.constants import WebhookSettings
from webhook.utils.types import WebhookEventMapping

tracer = Tracer()
router = APIGatewayRouter()
logger = Logger(child=True)


xero_mapping: Dict[str, WebhookEventMapping] = {
    "invoice": WebhookEventMapping(
        datalake_domain="finance",
        event_name="xeroInvoice"
    ),
}


@tracer.capture_method
def _verify_xero_signature(headers: Dict[str, str], body: str, webhook_key: str) -> Tuple[bool, str]:
    """
    Verify that the request is coming from Xero by checking the signature.

    Args:
        headers: The request headers containing the x-xero-signature
        body: The raw request body as a string
        webhook_key: The webhook signing key provided by Xero

    Returns:
        Tuple containing:
        - Boolean indicating if signature is valid
        - Message describing the result
    """
    try:
        xero_signature = headers.get("x-xero-signature")
        if not xero_signature:
            return False, "Missing x-xero-signature header"

        # Calculate HMACSHA256 hash of the payload using the webhook signing key
        calculated_hmac = hmac.new(
            key=webhook_key.encode(),
            msg=body.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Base64 encode the hash
        calculated_signature = base64.b64encode(calculated_hmac).decode()

        # Compare signatures
        if calculated_signature == xero_signature:
            return True, "Signature verification successful"
        else:
            return False, "Signature verification failed"
    except Exception as e:
        logger.error(f"Error verifying Xero signature: {str(e)}")
        return False, f"Error verifying signature: {str(e)}"


@router.post("/")
@tracer.capture_method
def process_xero_webhook():
    """
    Process incoming Xero webhook requests.

    All validation requests will contain:
    - Header: "x-xero-signature" with HMAC SHA256 hash value
    - Payload with events, lastEventSequence, firstEventSequence, and entropy

    Returns:
        - 2xx status for correctly signed payloads
        - 401 Unauthorized for incorrectly signed payloads
    """
    # Get the Lambda event and context from the decorator
    api_settings: WebhookSettings = router.context.get("api_settings", WebhookSettings())
    event = router.current_event

    # Get headers and body
    headers = event.headers
    body = event.body

    # Verify signature
    is_valid, message = _verify_xero_signature(headers, body, api_settings.xero_webhook_key)

    if not is_valid:
        logger.warning(f"Invalid Xero webhook signature: {message}")
        return Response(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            body=json.dumps({"message": "Unauthorized - Invalid signature"}),
            content_type=content_types.APPLICATION_JSON
        )

    # Process the webhook payload
    try:
        payload = json.loads(body)
        logger.info(f"Processing Xero webhook: {payload}")

        # TODO: Implement webhook processing logic here

        return Response(
            status_code=HTTPStatus.OK.value,
            body=json.dumps({"message": "Webhook received successfully"}),
            content_type=content_types.APPLICATION_JSON
        )
    except Exception as e:
        logger.error(f"Error processing Xero webhook: {str(e)}")
        return Response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            body=json.dumps({"message": f"Error processing webhook: {str(e)}"}),
            content_type=content_types.APPLICATION_JSON
        )
