import boto3

# Create client
client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

AGENT_ID = "4DC6IZL0VI"
AGENT_ALIAS_ID = "9O4WOM0UB2"
SESSION_ID = "user-001"


def chat_with_memory(user_input):
    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=SESSION_ID,   # 🔥 Memory linked here
        inputText=user_input
    )

    result = ""
    for event in response["completion"]:
        if "chunk" in event:
            result += event["chunk"]["bytes"].decode()

    return result


# First interaction (stores memory)
print(chat_with_memory("Hi, my name is Mohseena,I like roses"))

# Second interaction (uses memory)
print(chat_with_memory("What is my name?,which flower i like?"))
