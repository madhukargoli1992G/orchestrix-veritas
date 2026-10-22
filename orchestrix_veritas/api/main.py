from fastapi import FastAPI
from pydantic import BaseModel

from orchestrix_veritas.graph import OrchestrixGraph


API_VERSION = "1.0.0"


app = FastAPI(
    title="Orchestrix Veritas API",
    description=(
    "Advanced Multimodal Agentic RAG Platform for "
    "document understanding, hybrid retrieval, "
    "agent-orchestrated reasoning, and answer verification."
    ),
    version=API_VERSION,
)

graph = OrchestrixGraph()


class AskRequest(BaseModel):
    query: str
    file_paths: list[str] = []


@app.get("/")
def root():
    return {
        "message": "Orchestrix Veritas API is running.",
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "orchestrix-veritas-api",
        "version": API_VERSION,
    }


@app.get("/version")
def version():
    return {
        "version": API_VERSION,
        "name": "Orchestrix Veritas",
        "type": "Agentic Multimodal RAG Platform",
    }


@app.post("/ask")
def ask(request: AskRequest):
    state = graph.run(
        query=request.query,
        file_paths=request.file_paths,
    )

    return {
        "query": state.query,
        "answer": state.final_response.get("answer", state.answer),
        "sources": state.sources,
        "citations": state.citations,
        "confidence": state.confidence,
        "verified": state.verification.get("verified", False),
        "is_grounded": state.verification.get("is_grounded", False),
        "safe_to_return": state.safe_to_return,
        "warnings": state.guardrails.get("warnings", []),
        "workflow_events": state.events,
    }