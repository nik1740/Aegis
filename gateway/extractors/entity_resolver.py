"""
Entity Resolution — Vendor name normalization pipeline.

Three-step resolution:
1. Exact match against canonical vendor aliases (PostgreSQL jsonb index)
2. Fuzzy match using RapidFuzz (Levenshtein distance ≤ 2)
3. LLM fallback for unrecognized merchants
"""

import structlog
from rapidfuzz import fuzz, process

from extractors.schemas import EntityResolutionResult

logger = structlog.get_logger()


class EntityResolver:
    """Resolves raw merchant names to canonical vendor entities."""

    def __init__(self):
        # TODO: Load vendor aliases from PostgreSQL on init
        self._vendor_cache: dict[str, dict] = {}

    async def resolve(self, merchant_name_raw: str) -> EntityResolutionResult:
        """
        Resolve a raw merchant name to a canonical vendor.

        Pipeline:
        1. Exact match in alias cache
        2. Fuzzy match (Levenshtein distance ≤ 2)
        3. LLM fallback for unknown merchants

        Args:
            merchant_name_raw: Raw merchant name from VLM extraction.

        Returns:
            EntityResolutionResult with canonical name and match metadata.
        """
        normalized = merchant_name_raw.strip().lower()

        # Step 1: Exact match
        for vendor_id, vendor in self._vendor_cache.items():
            if normalized in [alias.lower() for alias in vendor.get("aliases", [])]:
                logger.info("entity_resolved", method="exact", merchant=merchant_name_raw)
                return EntityResolutionResult(
                    canonical_vendor_id=vendor_id,
                    canonical_name=vendor["canonical_name"],
                    match_method="exact",
                    match_score=1.0,
                    aliases_count=len(vendor.get("aliases", [])),
                )

        # Step 2: Fuzzy match
        all_aliases = []
        alias_to_vendor = {}
        for vendor_id, vendor in self._vendor_cache.items():
            for alias in vendor.get("aliases", []):
                all_aliases.append(alias)
                alias_to_vendor[alias] = (vendor_id, vendor["canonical_name"])

        if all_aliases:
            matches = process.extract(merchant_name_raw, all_aliases, scorer=fuzz.ratio, limit=1)
            if matches and matches[0][1] >= 85:  # 85% similarity threshold
                best_match = matches[0][0]
                vendor_id, canonical_name = alias_to_vendor[best_match]
                logger.info("entity_resolved", method="fuzzy", merchant=merchant_name_raw, score=matches[0][1])
                return EntityResolutionResult(
                    canonical_vendor_id=vendor_id,
                    canonical_name=canonical_name,
                    match_method="fuzzy",
                    match_score=matches[0][1] / 100.0,
                )

        # Step 3: LLM fallback
        logger.warning("entity_unresolved", merchant=merchant_name_raw, fallback="llm")
        # TODO: Implement LLM-based entity resolution fallback
        return EntityResolutionResult(
            canonical_name=merchant_name_raw,
            match_method="llm_fallback",
            match_score=0.5,
        )

    async def refresh_cache(self) -> None:
        """Reload vendor aliases from PostgreSQL."""
        # TODO: Query vendors table and populate self._vendor_cache
        logger.info("vendor_cache_refreshed", count=len(self._vendor_cache))
