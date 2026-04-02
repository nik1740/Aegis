"""
Notification Tools — Slack/email notification delivery.

Used by agents to send notifications to employees and finance managers
about expense decisions, remediation requests, and fraud alerts.
"""

import os

import structlog

logger = structlog.get_logger()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")


async def send_slack_message(channel: str, message: str, expense_id: str) -> dict:
    """
    Send a Slack notification.

    Args:
        channel: Slack channel or user ID.
        message: Message text.
        expense_id: Associated expense ID for tracking.

    Returns:
        Delivery status.
    """
    logger.info("slack_notification_sending", channel=channel, expense_id=expense_id)

    if not SLACK_BOT_TOKEN:
        logger.warning("slack_not_configured")
        return {"delivered": False, "reason": "SLACK_BOT_TOKEN not configured"}

    # TODO: Use slack-sdk to send message
    # from slack_sdk.web.async_client import AsyncWebClient
    # client = AsyncWebClient(token=SLACK_BOT_TOKEN)
    # response = await client.chat_postMessage(channel=channel, text=message)

    return {"delivered": False, "reason": "not_implemented"}


async def send_email_notification(to_email: str, subject: str, body: str) -> dict:
    """
    Send an email notification.

    Args:
        to_email: Recipient email address.
        subject: Email subject.
        body: Email body text.

    Returns:
        Delivery status.
    """
    logger.info("email_notification_sending", to=to_email, subject=subject)
    # TODO: Implement email sending (SMTP or API-based)
    return {"delivered": False, "reason": "not_implemented"}
