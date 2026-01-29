""" test edge functionality.

Edges control flow not data.
"""
import pytest
#from IPython.display import Image, display
import operator
from typing import Annotated, List, Literal, TypedDict
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    counter: int
    nlist: Annotated[List[str], operator.add]


def node_a(state: State) -> State:
    return 

def node_b(state: State) -> State:
    return State(nlist=["B"])

def node_c(state: State) -> State:
    return State(nlist=["C"])


def conditional_edge(state: State) -> Literal["b", "c", END]:
    select = state["nlist"][-1]
    if select == "b":
        return "b"
    elif select == "c":
        return "c"
    elif select == "q":
        return END

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
