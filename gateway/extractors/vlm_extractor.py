"""
VLM Extractor — Vision-Language Model receipt extraction.

Calls Gemini 1.5 Pro / GPT-4o to extract structured data from receipt images
and PDF invoices. Uses Instructor library for constrained JSON decoding
via Pydantic schema enforcement.
"""

import os
from typing import Optional

import structlog
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from extractors.schemas import ExtractedExpense

logger = structlog.get_logger()

# LLM provider configuration
VLM_PROVIDER = os.getenv("VLM_PROVIDER", "google")  # google | openai | anthropic


class VLMExtractor:
    """Extracts structured expense data from receipt images using VLMs."""

    def __init__(self):
        self.provider = VLM_PROVIDER
        # TODO: Initialize Instructor client with the configured VLM provider
        # self.client = instructor.from_openai(OpenAI()) or instructor.from_google(...)
        logger.info("vlm_extractor_initialized", provider=self.provider)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=30),
        retry=retry_if_exception_type((TimeoutError, ConnectionError)),
    )
    async def extract(self, image_bytes: bytes, filename: str) -> ExtractedExpense:
        """
        Extract structured expense data from a receipt image or PDF.

        Args:
            image_bytes: Raw bytes of the receipt image/PDF.
            filename: Original filename for content type inference.

        Returns:
            ExtractedExpense: Pydantic model with validated extraction results.
        """
        logger.info("vlm_extraction_started", filename=filename, provider=self.provider)

        # TODO: Implement VLM extraction using Instructor for schema enforcement
        # response = await self.client.chat.completions.create(
        #     model="gemini-1.5-pro" or "gpt-4o",
        #     response_model=ExtractedExpense,
        #     messages=[
        #         {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
        #         {"role": "user", "content": [{"type": "image", "data": image_bytes}]},
        #     ],
        # )

        raise NotImplementedError("VLM extraction not yet implemented")


# System prompt for VLM extraction
EXTRACTION_SYSTEM_PROMPT = """You are a financial document extraction system.
Extract all structured data from the provided receipt/invoice image.

Rules:
- Extract the exact merchant name as printed on the receipt
- Parse all line items with descriptions, quantities, and prices
- Identify the transaction date, currency, subtotal, tax, tip, and total
- Infer the expense category based on the merchant and items
- Report a confidence score (0.0 to 1.0) for the overall extraction quality
- List any warnings about uncertain extractions

Output MUST conform to the provided JSON schema exactly."""
