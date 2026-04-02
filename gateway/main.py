"""
Aegis Gateway — FastAPI Ingestion Service

Layer 1: Multi-modal receipt/invoice extraction gateway.
Handles file upload, VLM extraction, entity resolution, and routing
to the agent orchestration layer.
"""

import os
import uuid
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.expenses import router as expenses_router
from routes.webhooks import router as webhooks_router

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager."""
    logger.info("aegis_gateway_starting", version="0.1.0")
    # TODO: Initialize database connections
    # TODO: Initialize Redis connection pool
    # TODO: Initialize Neo4j driver
    yield
    logger.info("aegis_gateway_shutting_down")
    # TODO: Cleanup connections


app = FastAPI(
    title="Aegis — Semantic Spend Orchestrator",
    description="AI-powered corporate expense management gateway with GraphRAG policy enforcement",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(expenses_router, prefix="/api/v1/expenses", tags=["Expenses"])
app.include_router(webhooks_router, prefix="/api/v1/webhooks", tags=["Webhooks"])


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Liveness probe — confirms the service is running."""
    return {
        "status": "healthy",
        "service": "aegis-gateway",
        "version": "0.1.0",
    }


@app.get("/api/v1/health/dependencies", tags=["Health"])
async def dependency_health():
    """Readiness probe — checks all downstream dependencies."""
    # TODO: Implement actual health checks for PostgreSQL, Redis, Neo4j, LLM providers
    return {
        "status": "healthy",
        "dependencies": {
            "postgresql": {"status": "unknown", "latency_ms": None},
            "redis": {"status": "unknown", "latency_ms": None},
            "neo4j": {"status": "unknown", "latency_ms": None},
            "llm_providers": {"status": "unknown"},
        },
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
