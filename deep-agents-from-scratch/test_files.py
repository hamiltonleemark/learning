"""Virtual file system tools for agent state management.

Try openai model in this test.

This module provides tools for managing a virtual filesystem stored in agent state,
enabling context offloading and information persistence across agent interactions.
"""
import os
import logging
import pytest 
from dotenv import load_dotenv
from notebooks.utils import show_prompt, format_messages
import src.deep_agents_from_scratch.prompts
from src.deep_agents_from_scratch.file_tools import ls, read_file, write_file
from src.deep_agents_from_scratch.state import DeepAgentState, Todo, file_reducer
from typing import Annotated, NotRequired
from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from langchain.agents import AgentState

load_dotenv(os.path.join("..", ".env"), override=True)

import warnings
warnings.filterwarnings("ignore", message="LangSmith now uses UUID v7",
                        category=UserWarning,)


from src.deep_agents_from_scratch.prompts import (
    LS_DESCRIPTION,
    READ_FILE_DESCRIPTION,
    WRITE_FILE_DESCRIPTION,
)

@tool(description=LS_DESCRIPTION)
def ls(state: Annotated[DeepAgentState, InjectedState]) -> list[str]:
    """List all files in the virtual filesystem."""
    logging.info("Listing files in virtual filesystem")

    return list(state.get("files", {}).keys())


@tool(description=READ_FILE_DESCRIPTION, parse_docstring=True)
def read_file(file_path: str, state: Annotated[DeepAgentState, InjectedState],
              offset: int = 0, limit: int = 2000,) -> str:
    """Read file content from virtual filesystem with optional offset and limit.

    Args:
        file_path: Path to the file to read
        state: Agent state containing virtual filesystem (injected in tool node)
        offset: Line number to start reading from (default: 0)
        limit: Maximum number of lines to read (default: 2000)

    Returns:
        Formatted file content with line numbers, or error message if file not found
    """
    logging.info(f"Reading file '{file_path}' from virtual filesystem with offset {offset} and limit {limit}")
    files = state.get("files", {})
    if file_path not in files:
        return f"Error: File '{file_path}' not found"

    content = files[file_path]
    if not content:
        return "System reminder: File exists but has empty contents"

    lines = content.splitlines()
    start_idx = offset
    end_idx = min(start_idx + limit, len(lines))

    if start_idx >= len(lines):
        return f"Error: Line offset {offset} exceeds file length ({len(lines)} lines)"

    result_lines = []
    for i in range(start_idx, end_idx):
        line_content = lines[i][:2000]  # Truncate long lines
        result_lines.append(f"{i + 1:6d}\t{line_content}")

    return "\n".join(result_lines)


@tool(description=WRITE_FILE_DESCRIPTION, parse_docstring=True)
def write_file(file_path: str, content: str,
               state: Annotated[DeepAgentState, InjectedState],
               tool_call_id: Annotated[str, InjectedToolCallId],) -> Command:
    """Write content to a file in the virtual filesystem.

    Args:
        file_path: Path where the file should be created/updated
        content: Content to write to the file
        state: Agent state containing virtual filesystem (injected in tool node)
        tool_call_id: Tool call identifier for message response (injected in tool node)

    Returns:
        Command to update agent state with new file content
    """
    logging.info(f"Writing to file '{file_path}' in virtual filesystem with content length {len(content)}")
    files = state.get("files", {})
    files[file_path] = content
    return Command(
        update={
            "files": files,
            "messages": [
                ToolMessage(f"Updated file {file_path}", tool_call_id=tool_call_id)
            ],
        }
    )




# File usage instructions
FILE_USAGE_INSTRUCTIONS = """You have access to a virtual file system to help you retain and save context.                                  
## Workflow Process                                                                                            
1. **Orient**: Use ls() to see existing files before starting work                                             
2. **Save**: Use write_file() to store the user's request so that we can keep it for later                     
3. **Read**: Once you are satisfied with the collected sources, read the saved file and use it to ensure that you directly answer the user's question."""

# Add mock research instructions
SIMPLE_RESEARCH_INSTRUCTIONS = """IMPORTANT: Just make a single call to the web_search tool and use the result provided by the tool to answer the user's question."""

# Full prompt
INSTRUCTIONS = (
    FILE_USAGE_INSTRUCTIONS + "\n\n" + "=" * 80 + "\n\n" + SIMPLE_RESEARCH_INSTRUCTIONS
)

from IPython.display import Image, display
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
#from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent


# Mock search result
search_result = """The Model Context Protocol (MCP) is an open standard protocol developed
by Anthropic to enable seamless integration between AI models and external systems like
tools, databases, and other services. It acts as a standardized communication layer,
allowing AI models to access and utilize data from various sources in a consistent and
efficient manner. Essentially, MCP simplifies the process of connecting AI assistants
to external services by providing a unified language for data exchange. """


# Mock search tool
@tool(parse_docstring=True)
def web_search(query: str,):
    """Search the web for information on a specific topic.

    This tool performs web searches and returns relevant results
    for the given query. Use this when you need to gather information from
    the internet about any topic.

    Args:
        query: The search query string. Be specific and clear about what
               information you're looking for.

    Returns:
        Search results from search engine.

    Example:
        web_search("machine learning applications in healthcare")
    """
    logging.info(f"Performing web search for query: {query}")
    return search_result


def test_reducer_syntax():
    """ Learning how to user reducer. """

    dict1 = {'a': 1, 'b': 2, 'c': 3}
    dict2 = {'d': 4, 'e': 5, 'f': 6}

    dict3 = {**dict1, **dict2}
    print(dict3)


def test_file():
    #  show_prompt(LS_DESCRIPTION)
    #  show_prompt(READ_FILE_DESCRIPTION)
    # show_prompt(WRITE_FILE_DESCRIPTION)

    # Create agent using create_react_agent directly
    #model = init_chat_model(model="gpt-4.1-mini", temperature=0.0)
    model = init_chat_model(model="gpt-5", temperature=0.0)
    tools = [ls, read_file, write_file, web_search]

    # Create agent with system prompt
    agent = create_agent(model, tools, system_prompt=INSTRUCTIONS,
                         state_schema=DeepAgentState)
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Give me an overview of Model Context Protocol (MCP).",
                }
            ],
            "files": {},
        }
    )
    format_messages(result["messages"])
