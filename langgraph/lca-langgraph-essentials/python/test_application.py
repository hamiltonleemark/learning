""" learn how to write a real AI application. """
#  pylint: disable=line-too-long
#  pylint: disable=broad-exception-caught


import logging
import uuid
from typing import List, Literal, TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


load_dotenv()
llm = ChatOpenAI(model="gpt-5-mini")



SEARCH_RESULTS1 = "Our product comes in several amazing colors including red, purple and pink."
SEARCH_RESULTS2 = "Our current subscription of $15/month will decrease next month to $12/month if you sign up for a year membership."
SEARCH_RESULTS3 = "We here are M-H T-Shirt Company create customer t-shirts in various styles and colors."


class EmailClassification(TypedDict):
    """ Classification of customer email. """
    intent: Literal["question", "bug", "billing", "feature", "complex"]
    urgency: Literal["low", "medium", "high", "critical"]
    topic: str
    summary: str


class EmailAgentState(TypedDict):
    """ State for the email agent. """
    email_content: str
    sender_email: str
    email_id: str

    classification: EmailClassification | None
    ticket_id: str | None
    search_results: List[str] | None
    customer_history: dict | None
    draft_response: str | None

# Define nodes and edges.
def read_email(state: EmailAgentState) -> EmailAgentState:
    """Read incoming email and extract content. """

    logger.debug("Reading email from: %s", state['sender_email'])

def classify_intent(state: EmailAgentState) -> EmailAgentState:
    """Use LLM to classify email intent and urgency, then route accordingly"""

    logger.debug("classifying email content %s", state)

    # Create structured LLM that returns EmailClassification dict
    structured_llm = llm.with_structured_output(EmailClassification)

    classification_prompt = f"""
    Analyze this customer email and classify it:

    Email: {state['email_content']}
    From: {state['sender_email']}

    Provide classification, including intent, urgency, topic, and summary
    """

    # Get structured response directly as a dict
    classification = structured_llm.invoke(classification_prompt)

    # Store classification as a single dict in state
    return {"classification": classification}


def search_documentation(state: EmailAgentState) -> EmailAgentState:
    """Search knowledge base for relevant information"""
    logger.debug("search_documentation %s", state)

    # Build search query from classification
    classification = state.get('classification', {})
    query = f"{classification.get('intent', '')} {classification.get('topic', '')}"
    logger.debug("search_documentation %s", query)

    try:
        # Implement search logic here
        search_results = [
            SEARCH_RESULTS1,
            SEARCH_RESULTS2,
            SEARCH_RESULTS3,
        ]
    except Exception as earg:
        # For recoverable search errors, store error and continue
        search_results = [f"Search temporarily unavailable: {earg}"]

    return {"search_results": search_results} # Raw search results or error

def bug_tracking(state: EmailAgentState) -> EmailAgentState:
    """Create or update bug tracking ticket"""

    # Create ticket in your bug tracking system
    ticket_id = f"BUG_{uuid.uuid4()}"
    logging.debug("Created bug ticket %s for email %s", ticket_id, state['email_id'])

    return {"ticket_id": ticket_id}

def write_response(state: EmailAgentState) -> Command[Literal["human_review", "send_reply"]]:
    "Generate response using context and route based on quality"""

    classification = state.get('classification', {})

    # Format context from raw state data on demand
    context_sections = []

    if state.get('search_results'):
        # Format search results for the prompt
        formatted_docs = "\n".join([f"- {doc}" for doc in state['search_results']])
        context_sections.append(f"Relevant documentation:\n{formatted_docs}")

    if state.get('customer_history'):
        # Format customer data for the prompt
        context_sections.append(f"Customer tier: {state['customer_history'].get('tier', 'standard')}")

    # Build the prompt with formatted context
    draft_prompt = f"""
    Draft a response to this customer email:
    {state['email_content']}

    Email intent: {classification.get('intent', 'unkown')}
    Urgency level: {classification.get('urgency', 'medium')}

    {chr(10).join(context_sections)}

    Guidelines:
    - Be professional and helpful
    - Address their specific concern
    - Use the provided documentation when relevant
    - Be brief
    """

    response = llm.invoke(draft_prompt)

    # Determine if human review is needed based on urgency and intent
    needs_review = (
        classification.get('urgency') in ['high', 'critical'] or
        classification.get('intent') == 'complex'
    )

    # Route to the appropriate next node
    if needs_review:
        goto = "human_review"
        print("Needs approval")
    else:
        goto = "send_reply"

    return Command(
        update = {"draft_response": response.content},
        goto = goto
    )

def human_review(state: EmailAgentState) -> Command[Literal["send_reply", END]]:
    """Pause for human review using interrupt and route based on decision"""

    classification = state.get('classification', {})

    # Interrupt() must come first - any code before it will re-run on resume
    human_decision = interrupt({
        "email_id": state['email_id'],
        "original_email": state['email_content'],
        "draft_response": state.get('draft_response', ""),
        "urgency": classification.get('urgency'),
        "intent": classification.get('intent'),
        "action": "Please review and approve/edit this response"
    })

    # Now process the human's decision
    if human_decision.get("approved"):
        return Command(
            update = {"draft_response": human_decision.get("edited_response", state['draft_response'])},
            goto = "send_reply"
        )
    # Rejection means human will handle directly
    return Command(update = {}, goto = END)

def send_reply(state: EmailAgentState) -> EmailAgentState:
    """Send the email response"""
    # Integrate with a email service
    print(f"Sending reply: {state['draft_response'][:60]}...")
    return {}


def test_email_agent():
    """Test the email agent state graph end-to-end"""
    builder = StateGraph(EmailAgentState)

    # Add nodes
    builder.add_node("read_email", read_email)
    builder.add_node("classify_intent", classify_intent)
    builder.add_node("search_documentation", search_documentation)
    builder.add_node("bug_tracking", bug_tracking)
    builder.add_node("write_response", write_response)
    builder.add_node("human_review", human_review)
    builder.add_node("send_reply", send_reply)

    # Add edges
    builder.add_edge(START, "read_email")
    builder.add_edge("read_email", "classify_intent")
    builder.add_edge("classify_intent", "search_documentation")
    builder.add_edge("classify_intent", "bug_tracking")
    builder.add_edge("search_documentation", "write_response")
    builder.add_edge("bug_tracking", "write_response")
    builder.add_edge("send_reply", END)

    # Compile with checkpointer for persistence
    memory = InMemorySaver()
    app = builder.compile(checkpointer = memory)

    ##
    # Run this to see the graph.
    # image = Image(app.get_graph().draw_mermaid_png())
    # with open("email_agent_graph.png", "wb") as w_hndl:
    #    w_hndl.write(image.data)
    ##

    initial_state = {
        "email_content" : "Hello, I was charged twice for my subscription! This is urgent!",
        "sender_email": "mark_lee_hamilton@att.net",
        "email_id": "email_001",
    }

    config = {"configurable": {"thread_id": "customer_001"}}
    result = app.invoke(initial_state, config=config)
    logger.info("Draft ready for review: %s\n", result['draft_response'])
    human_response = Command(
        resume = {
            "approved": True,
        }
    )
    final_result = app.invoke(human_response, config)
    logging.info("Final state: %s", final_result)
    logger.info("Email sent successfully")


def test_email_bulk():
    """Test bulk email response. """

    builder = StateGraph(EmailAgentState)

    # Add nodes
    builder.add_node("read_email", read_email)
    builder.add_node("classify_intent", classify_intent)
    builder.add_node("search_documentation", search_documentation)
    builder.add_node("bug_tracking", bug_tracking)
    builder.add_node("write_response", write_response)
    builder.add_node("human_review", human_review)
    builder.add_node("send_reply", send_reply)

    # Add edges
    builder.add_edge(START, "read_email")
    builder.add_edge("read_email", "classify_intent")
    builder.add_edge("classify_intent", "search_documentation")
    builder.add_edge("classify_intent", "bug_tracking")
    builder.add_edge("search_documentation", "write_response")
    builder.add_edge("bug_tracking", "write_response")
    builder.add_edge("send_reply", END)

    # Compile with checkpointer for persistence
    memory = InMemorySaver()
    app = builder.compile(checkpointer = memory)

    ##
    # Run this to see the graph.
    # image = Image(app.get_graph().draw_mermaid_png())
    # with open("email_agent_graph.png", "wb") as w_hndl:
    #    w_hndl.write(image.data)
    ##

    email_content = [
        "My subscription is going to end in a few months, what is the new rate?",
        "The tire won't stay on my car!",
        "Can you tell me how long the sale is on?",
        "I was wondering if your t-shirts are available in blue?",
        "I was charged twice for my subscription! This is urgent!",
    ]

    needs_approval = []


    for item, content in enumerate(email_content):
        initial_state = {
            "email_content" : content,
            "sender_email": "mark_lee_hamilton@att.net",
            "email_id": f"email_{item}",
        }
        print(f"{initial_state['email_id']}: ", end="")

        thread_id = uuid.uuid4()
        config = {"configurable": {"thread_id": str(thread_id)}}
        result = app.invoke(initial_state, config=config)
        print(result)

        if "__interrupt__" in result.keys():
            result['thread_id'] = thread_id
            needs_approval.append(result)

        return
