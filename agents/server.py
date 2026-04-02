"""
Agent Server — FastAPI server for the LangGraph agent orchestration service.

Exposes endpoints for:
- Triggering expense evaluation via the agent graph
- Querying agent execution status
- Health checks
"""

import os
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle."""
    logger.info("agent_server_starting", version="0.1.0")
    # TODO: Initialize LangGraph with PostgreSQL checkpointer
    # TODO: Initialize LLM clients (OpenAI, Anthropic, Google)
    yield
    logger.info("agent_server_shutting_down")


app = FastAPI(
    title="Aegis Agent Server",
    description="LangGraph multi-agent orchestration for expense auditing",
    version="0.1.0",
)


class EvaluateRequest(BaseModel):
    """Request to evaluate an expense through the agent pipeline."""
    expense_id: str
    employee_id: str
    extracted_data: dict
    justification: str


class EvaluateResponse(BaseModel):
    """Response from the agent evaluation."""
    expense_id: str
    status: str
    decision: str | None = None
    trace_id: str | None = None


@app.post("/api/v1/evaluate", response_model=EvaluateResponse)
async def evaluate_expense(request: EvaluateRequest):
    """
    Trigger the multi-agent evaluation pipeline for an expense.

    Routes through: extract_policy → auditor + fraud detective → compliance judge
    """
    logger.info("evaluation_requested", expense_id=request.expense_id)

    # TODO: Run the LangGraph expense graph
    # from graph import expense_graph_builder
    # graph = expense_graph_builder.compile(checkpointer=checkpointer)
    # result = await graph.ainvoke({...})

    return EvaluateResponse(
        expense_id=request.expense_id,
        status="PROCESSING",
    )


@app.get("/api/v1/status/{expense_id}")
async def get_evaluation_status(expense_id: str):
    """Check the status of an ongoing agent evaluation."""
    # TODO: Query LangGraph checkpointer for current state
    return {"expense_id": expense_id, "status": "unknown"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "aegis-agent-server"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8100, reload=True)
