from orchestrix_veritas.graph import OrchestrixGraph


def test_orchestrix_graph_exposes_langgraph_builder():
    graph = OrchestrixGraph()

    assert hasattr(graph, "build_langgraph")
    assert callable(graph.build_langgraph)


def test_orchestrix_graph_langgraph_builder_is_safe_without_dependency():
    graph = OrchestrixGraph()

    compiled_graph = graph.build_langgraph()

    assert compiled_graph is None or hasattr(compiled_graph, "invoke")