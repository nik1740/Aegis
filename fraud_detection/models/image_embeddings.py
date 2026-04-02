"""
Image Embeddings — CLIP-based duplicate receipt detection.

Uses CLIP ViT-B/32 to generate 512-dimensional embeddings for receipt images.
Embeddings are stored in ChromaDB and queried for near-duplicate detection.

Duplicate detection threshold: cosine similarity > 0.95
"""

from pathlib import Path
from typing import Optional

import numpy as np
import structlog

logger = structlog.get_logger()


class ImageEmbedder:
    """CLIP-based image embedding generator for duplicate detection."""

    def __init__(self):
        self.model = None
        self.processor = None
        self._initialized = False

    def _lazy_init(self) -> None:
        """Lazy-load the CLIP model (heavy, only when needed)."""
        if self._initialized:
            return

        try:
            from transformers import CLIPModel, CLIPProcessor

            self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            self._initialized = True
            logger.info("clip_model_loaded", model="openai/clip-vit-base-patch32")
        except Exception as e:
            logger.error("clip_model_load_failed", error=str(e))
            raise

    def embed(self, image_bytes: bytes) -> np.ndarray:
        """
        Generate a 512-dimensional CLIP embedding for a receipt image.

        Args:
            image_bytes: Raw bytes of the receipt image.

        Returns:
            NumPy array of shape (512,) — the image embedding.
        """
        self._lazy_init()

        from io import BytesIO
        from PIL import Image

        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")

        import torch
        with torch.no_grad():
            outputs = self.model.get_image_features(**inputs)

        embedding = outputs.squeeze().numpy()
        # Normalize to unit vector for cosine similarity
        embedding = embedding / np.linalg.norm(embedding)

        logger.info("image_embedded", embedding_dim=embedding.shape[0])
        return embedding

    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector.
            embedding2: Second embedding vector.

        Returns:
            Cosine similarity score (0.0 to 1.0).
        """
        similarity = float(np.dot(embedding1, embedding2))
        return round(similarity, 4)

    def is_duplicate(self, embedding1: np.ndarray, embedding2: np.ndarray, threshold: float = 0.95) -> bool:
        """
        Check if two receipt images are duplicates.

        Args:
            embedding1: First image embedding.
            embedding2: Second image embedding.
            threshold: Similarity threshold for duplicate detection (default 0.95).

        Returns:
            True if images are considered duplicates.
        """
        similarity = self.compute_similarity(embedding1, embedding2)
        is_dup = similarity >= threshold
        if is_dup:
            logger.warning("duplicate_detected", similarity=similarity, threshold=threshold)
        return is_dup
