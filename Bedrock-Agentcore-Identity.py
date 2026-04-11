import boto3

client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")

AGENT_ID = "BUGNBMI0PV"
ALIAS_ID = "AVYY4XZVCI"

def chat(user_id, message):
    session_id = f"session-{user_id}"   # identity mapping

    response = client.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=ALIAS_ID,
        sessionId=session_id,
        inputText=message
    )

    output = ""
    for event in response.get("completion", []):
        if "chunk" in event:
            output += event["chunk"]["bytes"].decode()

    return output


# Different users
print(chat("user1", "Hi, my name is Mohseena"))
print(chat("user1", "What is my name?"))  # remembers

print(chat("user2", "What is my name?"))  # new user, no memory
