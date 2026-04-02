"""
CRM Tools — LangGraph tools for CRM validation.

Used by the Remediation Agent to validate client meeting claims
against CRM systems (Salesforce, HubSpot, etc.).
"""

import os

import httpx
import structlog

logger = structlog.get_logger()

CRM_API_URL = os.getenv("CRM_API_URL", "https://api.hubspot.com/crm/v3")
CRM_API_KEY = os.getenv("CRM_API_KEY", "")


async def validate_client_contact(client_name: str, company_name: str) -> dict:
    """
    Validate a client contact against the CRM system.

    Used by the Remediation Agent to verify client meeting claims
    when employees invoke the client_meeting exemption.

    Args:
        client_name: Name of the client (e.g., "Jane Doe")
        company_name: Company name (e.g., "Acme Corp")

    Returns:
        Dictionary with validation result and contact details.
    """
    logger.info("crm_validation_requested", client=client_name, company=company_name)

    # TODO: Implement actual CRM API call
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(
    #         f"{CRM_API_URL}/contacts/search",
    #         headers={"Authorization": f"Bearer {CRM_API_KEY}"},
    #         params={"query": client_name},
    #     )
    #     contacts = response.json()

    # Mock response for development
    return {
        "validated": False,
        "client_name": client_name,
        "company_name": company_name,
        "status": "not_implemented",
        "message": "CRM integration not yet configured",
    }
