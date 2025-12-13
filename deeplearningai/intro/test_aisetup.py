""" Test numpy samples. """
import os
from dotenv import load_dotenv
from openai import OpenAI
import aisetup


def test_openai():
    """ Test the nump module functionality. """
    load_dotenv(".env", override=True)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key, "OPENAI_API_KEY is not set in environment variables."

    client = OpenAI(api_key=openai_api_key)
    assert client, "Failed to create OpenAI client."


def test_deeplearning():
    """ Test the nump module functionality. """

    load_dotenv(".env", override=True)
    openai_api_key = os.getenv("OPENAI_API_KEY")
    assert openai_api_key, "OPENAI_API_KEY is not set in environment variables."

    aisetup.authenticate(openai_api_key)
    response = aisetup.get_llm_response("What is the capital of MN.")
    print("LLM Response:", response)
