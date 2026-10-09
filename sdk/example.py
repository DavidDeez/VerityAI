import os
from verityai import VerityAI

# Assuming you've created a project and generated an API key via the API
API_KEY = os.getenv("RELIANTAI_API_KEY", "your_api_key_here")

client = VerityAI(api_key=API_KEY)

# Approach 1: Manual Tracing
print("Sending manual trace...")
trace = client.trace(
    model="gpt-4",
    provider="openai",
    input="What is your refund policy?"
)

# Simulate LLM call
output = "Customers can request refunds within 30 days."

trace.log_output(
    output=output,
    input_tokens=15,
    output_tokens=10,
    cost=0.001
)

trace.finish(status="success")
print(f"Trace logged with ID: {trace.id}")

# Approach 2: Decorator Tracing
print("Testing decorator trace...")
@client.observe(model="local-model", provider="ollama")
def ask_agent(question: str):
    return f"This is a simulated response to: {question}"

try:
    response = ask_agent("How do I reset my password?")
    print(f"Agent response: {response}")
except Exception as e:
    print(f"Agent error: {e}")
