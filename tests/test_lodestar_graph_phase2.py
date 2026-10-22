from orchestrix_veritas.graph import OrchestrixGraph


def test_orchestrix_graph_has_phase2_nodes():
    graph = OrchestrixGraph()

    assert hasattr(graph, "query_rewrite_agent")
    assert hasattr(graph, "context_evaluator_agent")
    assert hasattr(graph, "rag_guardrails")
    assert hasattr(graph, "safe_response_formatter")


def test_orchestrix_graph_rewrite_query_node_updates_state():
    graph = OrchestrixGraph()

    from orchestrix_veritas.state import RAGState

    state = RAGState(
        query="What increased in 2024?",
        retry_count=1,
    )

    result = graph.rewrite_query_node(state)

    assert result.rewritten_query
    assert "financial" in result.rewritten_query
    assert result.active_query == result.rewritten_query
    assert "rewrite_query_node_completed" in result.events


def test_orchestrix_graph_context_evaluator_node_updates_state():
    graph = OrchestrixGraph()

    from orchestrix_veritas.state import RAGState

    state = RAGState(
        query="What increased in 2024?",
        retrieved_chunks=[
            {
                "text": "Revenue increased by 25% in 2024.",
                "score": 0.95,
            }
        ],
    )

    result = graph.evaluate_context_node(state)

    assert result.context_sufficient is True
    assert result.retrieved_count == 1
    assert "evaluate_context_node_completed" in result.events