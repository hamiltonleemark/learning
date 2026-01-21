""" Learning how to connect to bedrock models. """

# pylint: disable=broad-exception-caught

import sys
import json
import logging
import boto3
from botocore.exceptions import ClientError

def test_bedrock_converse():
    """ Example on how to invoke boto3.conversem method. """

    bedrock_runtime = boto3.client('bedrock-runtime')
    assert bedrock_runtime
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    prompt = "Tell me the capital of France."

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": prompt
                }
            ]
        }
    ]

    # Optional inference parameters

    inference_config = {
        "maxTokens": 300,
        "temperature": 0.7,
        "topP": 0.9,
    }
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=messages,
        inferenceConfig=inference_config)
    assert response
    logging.debug(json.dumps(response, indent=4))
    assert "Paris" in response["output"]["message"]["content"][0]["text"]


def test_bedrock_invoke_model():
    """ Example on invoking bedrock-runtime invoke_model API."""

    bedrock_runtime = boto3.client('bedrock-runtime')
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    prompt = "Tell me the capital of France."

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        resp = bedrock_runtime.invoke_model(modelId=model_id, body=request)
        assert resp

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        sys.exit(1)

    body = json.loads(resp.get("body").read().decode("utf-8"))
    logging.debug(body)
    assert "Paris" in body["content"][0]["text"]


def test_bedrock_stop_reason_max_tokens():
    """ Invoke the mode and check to see we reached max_tokens. """

    bedrock_runtime = boto3.client('bedrock-runtime')
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    prompt = "Write a summary of Las Vegas. """

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 50,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        resp = bedrock_runtime.invoke_model(modelId=model_id, body=request)
        assert resp

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        sys.exit(1)

    body = json.loads(resp.get("body").read().decode("utf-8"))
    logging.debug(body)
    assert "Las Vegas" in body["content"][0]["text"]
    assert body["stop_reason"] == "max_tokens"


def test_bedrock_stop_reason_end_turn():
    """ Invoke model and check for a long response finishes correctly. """

    bedrock_runtime = boto3.client('bedrock-runtime')
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"

    prompt = "Write a summary of Las Vegas. """

    native_request = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    # Convert the native request to JSON.
    request = json.dumps(native_request)

    try:
        # Invoke the model with the request.
        resp = bedrock_runtime.invoke_model(modelId=model_id, body=request)
        assert resp

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        sys.exit(1)

    body = json.loads(resp.get("body").read().decode("utf-8"))
    logging.debug(body)
    assert "Las Vegas" in body["content"][0]["text"]
    assert body["stop_reason"] == "end_turn"
