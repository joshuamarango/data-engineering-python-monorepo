import hmac
import datetime
import hashlib
import base64
import json

import requests
from http import HTTPStatus
from pydantic import BaseModel
from typing import Dict, List, Tuple

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.event_handler import Response, content_types
from aws_lambda_powertools.event_handler.router import APIGatewayRouter

from webhook.utils.constants import EnvironmentVariables
from webhook.utils.types import WebhookEventMapping

tracer = Tracer()
router = APIGatewayRouter()
logger = Logger(child=True)


class XeroParams(BaseModel):
    xero_webhook_key: str
    xero_access_token: str


class XeroEvent(BaseModel):
    resourceUrl: str
    resourceId: str
    eventType: str
    eventCategory: str
    eventDate: datetime.datetime
    tenantId: str
    tenantType: str


class XeroWebhookPayload(BaseModel):
    events: List[XeroEvent]
    firstEventSequence: int
    lastEventSequence: int
    entropy: str


xero_mapping: Dict[str, WebhookEventMapping] = {
    "invoice": WebhookEventMapping(
        datalake_domain="finance",
        event_name="xeroInvoice"
    ),
    "contact": WebhookEventMapping(
        datalake_domain="customer",
        event_name="xeroContact"
    ),
    "subscription": WebhookEventMapping(
        datalake_domain="customer",
        event_name="xeroSubscription"
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


@tracer.capture_method
def _fetch_xero_resource(resource_url: str, access_token: str) -> Dict:
    """
    Fetch resource data from Xero API.

    Args:
        resource_url: The Xero API endpoint URL
        access_token: OAuth 2.0 access token for Xero API

    Returns:
        Response data from Xero API as dictionary
    """
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }
        
        response = requests.get(resource_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching from Xero API: {str(e)}")
        return {"error": str(e)}


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
    env_vars: EnvironmentVariables = router.context.get("env_vars", EnvironmentVariables())
    xero_params: XeroParams = XeroParams(**parameters.get_parameter(name=env_vars.ssm_param_xero, transform="json"))
    event = router.current_event

    # Get headers and body
    headers = event.headers

    # Verify signature
    is_valid, message = _verify_xero_signature(headers=headers, body=event.body, webhook_key=xero_params.xero_webhook_key)

    if not is_valid:
        logger.warning(f"Invalid Xero webhook signature: {message}")
        return Response(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            body=json.dumps({"message": "Unauthorized - Invalid signature"}),
            content_type=content_types.APPLICATION_JSON
        )

    # Process the webhook payload
    try:
        payload = event.json_body
        logger.info(f"Processing Xero webhook: {payload}")

        # Parse the payload using the Pydantic model
        webhook_data = XeroWebhookPayload(**payload)
        
        # Process each event in the webhook
        for event in webhook_data.events:
            logger.debug(event)

            # Map the event to the webhook event mapping
            webhook_event_mapping = xero_mapping.get(event.eventType)
            if not webhook_event_mapping:
                logger.warning(f"No webhook event mapping found for event type: {event.eventCategory.lower()}")
                continue
            
            # Call Xero API using the resourceUrl
            resource_data = _fetch_xero_resource(
                resource_url=event.resourceUrl, 
                access_token=xero_params.xero_access_token
            )
            
            # Log the API response
            logger.info(f"Xero API response for {event.resourceId}: {resource_data}")
            
            # TODO: Process resource data further if needed
            # For example, add to a queue, store in database, etc.

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
