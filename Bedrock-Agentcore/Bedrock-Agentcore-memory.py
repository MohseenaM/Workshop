import boto3
import json

# Create AgentCore client
client = boto3.client(
    "bedrock-agent-runtime",
    region_name="us-east-1"
)

# Unique session ID (per user)
session_id = "memory-user-001"

# -----------------------------
# 1. STORE MEMORY
# -----------------------------
def store_memory(session_id, key, value):
    response = client.put_session(
        sessionId=session_id,
        sessionState={
            "sessionAttributes": {
                key: value
            }
        }
    )
    return response


# -----------------------------
# 2. GET MEMORY
# -----------------------------
def get_memory(session_id):
    response = client.get_session(
        sessionId=session_id
    )
    return response.get("sessionState", {})


# -----------------------------
# 3. DELETE MEMORY (optional)
# -----------------------------
def delete_memory(session_id):
    response = client.delete_session(
        sessionId=session_id
    )
    return response


# -----------------------------
# TEST MEMORY
# -----------------------------
if __name__ == "__main__":

    # Store memory
    store_memory(session_id, "name", "Mohseena")
    store_memory(session_id, "city", "Nashik")

    # Retrieve memory
    memory = get_memory(session_id)

    print("\nStored Memory:")
    print(json.dumps(memory, indent=2))

    # Optional delete
    # delete_memory(session_id)
