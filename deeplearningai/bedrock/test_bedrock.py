import sys
import boto3
import json
from botocore.exceptions import ClientError

def test_bedrock():

    bedrock_runtime = boto3.client('bedrock-runtime')
    assert bedrock_runtime
    modelId = "anthropic.claude-3-sonnet-20240229-v1:0"

    prompt = "Tell me the capital of Frane."

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
        modelId=modelId,
        messages=messages,
        inferenceConfig=inference_config)
    assert response
    print(json.dumps(response, indent=4))

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
        resp = bedrock_runtime.invoke_model(modelId=modelId, body=request)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{modelId}'. Reason: {e}")
        sys.exit(1)

    print(json.dumps(resp.get("body").read().decode("utf-8"), indent=4))
