""" test edge functionality.

Edges control flow not data.
"""
import operator
from typing import Annotated, List, TypedDict
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    """ state definition """
    counter: int
    nlist: Annotated[List[str], operator.add]


def node_a(state: State) -> State:
    """ node a """
    print(f"node a received {state['nlist']}")
    return State(nlist=["A"])

def node_b(state: State) -> State:
    """ node b """
    print(f"node b received {state['nlist']}")
    return State(nlist=["B"])

def node_c(state: State) -> State:
    """ node c """
    print(f"node c received {state['nlist']}")
    return State(nlist=["C"])

def node_bb(state: State) -> State:
    """ node bb """
    print(f"node bb received {state['nlist']}")
    return State(nlist=["BB"])

def node_cc(state: State) -> State:
    """ node cc """
    print(f"node cc received {state['nlist']}")
    return State(nlist=["CC"])

def node_d(state: State) -> State:
    """ node d """
    print(f"node d received {state['nlist']}")
    return State(nlist=["D"])


def test_edge_merge():
    """ test edge functionality.

    Nodes see all data. node_bb sees node_c data.
    """

    build = StateGraph(State)
    build.add_node("a", node_a)
    build.add_node("b", node_b)
    build.add_node("c", node_c)
    build.add_node("bb", node_bb)
    build.add_node("cc", node_cc)
    build.add_node("d", node_d)

    build.add_edge(START, "a")
    build.add_edge("a", "b")
    build.add_edge("a", "c")
    build.add_edge("b", "bb")
    build.add_edge("c", "cc")
    build.add_edge("bb", "d")
    build.add_edge("cc", "d")
    build.add_edge("d", END)

    graph = build.compile()
    initial_state = State(nlist=["Initial String"])
    resp = graph.invoke(initial_state)
    print(resp)
    assert resp["nlist"] == ['Initial String', 'A', 'B', 'C', 'BB', 'CC', 'D']


def test_edge_no_d():
    """ test edge functionality. """

    build = StateGraph(State)
    build.add_node("a", node_a)
    build.add_node("b", node_b)
    build.add_node("c", node_c)
    build.add_node("bb", node_bb)
    build.add_node("cc", node_cc)
    build.add_node("d", node_d)

    build.add_edge(START, "a")
    build.add_edge("a", "b")
    build.add_edge("a", "c")
    build.add_edge("b", "bb")
    build.add_edge("c", "cc")
    build.add_edge("bb", END)
    build.add_edge("cc", END)

    graph = build.compile()
    initial_state = State(nlist=["Initial String"])
    resp = graph.invoke(initial_state)
    print(resp)
    assert resp["nlist"] == ['Initial String', 'A', 'B', 'C', 'BB', 'CC']
