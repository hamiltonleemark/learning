""" test simple nodes in a state graph. """

from typing import List, TypedDict
from langgraph.graph import END, START, StateGraph

class State(TypedDict):
    """ state object for the graph. """
    counter: int
    nlist: List[str]


def node_a(state: State) -> State:
    """ Node function needs to return a state object. """
    print(f"node a received {state['nlist']}")
    note = "Hello World from Node a"
    ##
    # This works. Curious to see if I can return the input state with modifications.
    #return State(nlist = [note]), counter=state['counter'])
    #
    # Yes, I can. Not sure why would would construct a new object
    # documentation states that langgraph merges state.
    #return state
    return {"nlist": [note], "counter": state["counter"] + 1}


def node_b(state: State) -> State:
    """ Node function needs to return a state object. """
    print(f"node b received {state['nlist']}")
    note = "Hello World from Node b"
    nlist = state["nlist"] + [note]
    return {"nlist": nlist, "counter": state["counter"] + 1}


def test_node_a():
    """ test two nodes. """

    build = StateGraph(State)
    build.add_node("a", node_a)
    build.add_node("b", node_b)
    build.add_edge("a", "b")
    build.add_edge(START, "a")
    build.add_edge("b", END)
    graph = build.compile()

    initial_state = State(nlist=["Hello Node a, how are you?"], counter=0)
    resp = graph.invoke(initial_state)
    print(resp)
    print("counter: ", resp["counter"])
    assert resp["counter"] == 2
    assert "Hello World from Node a" in resp["nlist"]
    assert "Hello World from Node b" in resp["nlist"]
