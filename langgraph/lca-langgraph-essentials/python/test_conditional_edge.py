""" test edge functionality.

Edges control flow not data.
"""
import logging
import operator
from typing import Annotated, List, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt


class State(TypedDict):
    """ Holds state of the graph. """
    counter: int
    nlist: Annotated[List[str], operator.add]


def node_a(state: State) -> State:
    """ Node a. """
    logging.info("node_a state before: %s", state)
    return state

def node_b(state: State) -> State:
    """ Node b. """
    logging.info("node_b state before: %s", state)

    return State(nlist=["B"])

def node_c(state: State) -> State:
    """ Node c. """
    logging.info("node_c state before: %s", state)
    return State(nlist=["C"])


def conditional_edge(state: State) -> Literal["b", "c", END]:
    """ Conditional edge from a to b or c. """
    select = state["nlist"][-1]
    if select == "b":
        return "b"

    if select == "c":
        return "c"

    if select == "q":
        return END
    raise interrupt(f"invalid selection: {select}")

def test_edge_merge():
    """ test edge functionality.

    Nodes see all data. node_bb sees node_c data.
    """

    build = StateGraph(State)
    build.add_node("a", node_a)
    build.add_node("b", node_b)
    build.add_node("c", node_c)

    build.add_edge(START, "a")
    build.add_edge("b", END)
    build.add_edge("c", END)
    build.add_conditional_edges("a", conditional_edge)

    graph = build.compile()

    #user = input('b, c or q:')
    user = 'b'
    initial_state = State(nlist=[user])
    resp = graph.invoke(initial_state)
    print(resp)
    assert resp["nlist"] == ['b', 'B']
