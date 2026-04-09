import boto3
import json

client = boto3.client("bedrock-runtime", region_name="us-east-1")

response = client.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307",
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "anthropic_version": "bedrock-2023-05-31",  # ✅ REQUIRED
        "messages": [
            {
                "role": "user",
                "content": "Give a short motivational quote."
            }
        ],
        "max_tokens": 100
    })
)

result = json.loads(response["body"].read())
print(result["content"][0]["text"])
