""" test edge functionality.

Edges control flow not data.
"""
import logging
import operator
from typing import Annotated, List, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt


class State(TypedDict):
    """ state for the graph. """
    counter: int
    nlist: Annotated[List[str], operator.add]


def node_a(state: State) -> State:
    """ node a adds its name to the list and returns the state. """
    logging.info("node_a received state: %s", state)
    return state

def node_b(state: State) -> State:
    """ node b adds its name to the list and returns the state. """
    logging.info("node_b received state: %s", state)
    return State(nlist=["B"])

def node_c(state: State) -> State:
    """ node c adds its name to the list and returns the state. """
    logging.info("node_c received state: %s", state)

    return State(nlist=["C"])


def conditional_edge(state: State) -> Literal["b", "c", END]:
    """ conditional edge based on user input. """

    select = state["nlist"][-1]

    if select == "b":
        return "b"

    if select == "c":
        return "c"

    if select == "q":
        return END
    raise interrupt(f"invalid selection: {select}")

def test_memory():
    """ test edge functionality.

    Nodes see all data. node_bb sees node_c data.
    """

    ##
    # build graph
    memory = InMemorySaver()
    config1 = {"configurable": {"thread_id": "1"}}

    build = StateGraph(State)
    build.add_node("a", node_a)
    build.add_node("b", node_b)
    build.add_node("c", node_c)

    build.add_edge(START, "a")
    build.add_edge("b", END)
    build.add_edge("c", END)
    build.add_conditional_edges("a", conditional_edge)

    graph = build.compile(checkpointer=memory)

    #user = input('b, c or q:')
    user = 'b'
    initial_state = State(nlist=[user])
    resp = graph.invoke(initial_state, config1)
    print(resp)
    assert resp["nlist"] == ['b', 'B']

    user = 'c'
    initial_state = State(nlist=[user])
    resp = graph.invoke(initial_state, config1)
    print(resp)
    assert resp["nlist"] == ['b', 'B', 'c', 'C']
    ##

    config2 = {"configurable": {"thread_id": "2"}}
    user = 'b'
    initial_state = State(nlist=[user])
    resp = graph.invoke(initial_state, config2)
    print(resp)
    assert resp["nlist"] == ['b', 'B']

    user = 'b'
    initial_state = State(nlist=[user])
    resp = graph.invoke(initial_state, config1)
    print(resp)
    assert resp["nlist"] == ['b', 'B', 'c', 'C', 'b', 'B']
