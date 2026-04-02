"""
Pydantic Schemas — Structured output models for the ingestion pipeline.

These schemas are used with Instructor for constrained VLM decoding,
ensuring the LLM cannot return malformed output.
"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class ExpenseCategory(str, Enum):
    """Valid expense categories."""
    MEALS = "meals"
    TRANSPORT = "transport"
    ACCOMMODATION = "accommodation"
    OFFICE_SUPPLIES = "office_supplies"
    CLIENT_ENTERTAINMENT = "client_entertainment"
    CONFERENCE = "conference"
    OTHER = "other"


class LineItem(BaseModel):
    """Individual line item from a receipt."""
    description: str
    quantity: int = 1
    unit_price: float
    total: float


class ExtractedExpense(BaseModel):
    """
    Schema enforced via constrained decoding on the VLM output.

    This model represents the structured extraction from a receipt image,
    validated at the API boundary before entering the agent pipeline.
    """
    merchant_name_raw: str = Field(..., description="Exact merchant name as printed")
    merchant_name_canonical: str | None = Field(None, description="Resolved after entity normalization")
    merchant_address: str | None = None
    transaction_date: date
    currency: str = Field(..., pattern=r"^[A-Z]{3}$", description="ISO 4217 currency code")
    subtotal: float
    tax_amount: float | None = None
    tip_amount: float | None = None
    total_amount: float
    payment_method: str | None = None
    line_items: list[LineItem] = []
    category_inferred: ExpenseCategory
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    extraction_warnings: list[str] = []


class EntityResolutionResult(BaseModel):
    """Result of vendor entity resolution."""
    canonical_vendor_id: str | None = None
    canonical_name: str
    match_method: str  # exact | fuzzy | llm_fallback
    match_score: float = Field(..., ge=0.0, le=1.0)
    aliases_count: int = 0
