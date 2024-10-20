def test_connection(knowledge_graph):
    node = knowledge_graph.create_node(
        "TestNode", {"test_key": "test_value1", "test_key2": "test_value2"}
    )
    assert node is not None

    fetched_node = knowledge_graph.get_node("TestNode", {"test_key": "test_value1"})
    assert fetched_node is not None

    assert fetched_node["test_key"] == "test_value1"
    assert fetched_node["test_key2"] == "test_value2"
