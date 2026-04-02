"""
Webhook Routes — External integration endpoints.

Handles:
- Slack event callbacks
- n8n workflow triggers
- External system notifications
"""

import structlog
from fastapi import APIRouter, Request

logger = structlog.get_logger()
router = APIRouter()


@router.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack event callbacks (challenge verification + message events)."""
    body = await request.json()

    # Slack URL verification challenge
    if body.get("type") == "url_verification":
        return {"challenge": body["challenge"]}

    # TODO: Process Slack events (employee responses to remediation messages)
    logger.info("slack_event_received", event_type=body.get("type"))
    return {"status": "ok"}


@router.post("/n8n/trigger")
async def n8n_trigger(request: Request):
    """Handle n8n workflow triggers (batch processing, scheduled tasks)."""
    body = await request.json()
    # TODO: Process n8n workflow triggers
    logger.info("n8n_trigger_received", workflow=body.get("workflow"))
    return {"status": "ok"}
