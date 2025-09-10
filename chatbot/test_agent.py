from strands import Agent
from strands.models import BedrockModel # <-- Make sure to import BedrockModel
import logging

# Configure logging
logging.basicConfig(format="%(levelname)s | %(name)s | %(message)s", handlers=[logging.StreamHandler()])
logging.getLogger("strands").setLevel(logging.DEBUG)

# Define the model and a supported region
CLAUDE_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"
AWS_REGION = "us-west-2"

# --- Step 1: Create and configure the model object ---
# The region is passed in a 'config' dictionary to the model itself.
# Note that the key is 'region_name', which is standard for the underlying AWS client.
bedrock_model = BedrockModel(
    model_id=CLAUDE_MODEL_ID,
    config={"region_name": AWS_REGION}
)

# --- Step 2: Pass the configured model object to the Agent ---
agent = Agent(
    system_prompt="You are a helpful AI assistant that answers questions.",
    model=bedrock_model # <-- Pass the model object here, not the ID string
)

# This should now work correctly
try:
    response = agent("What is Strands Agents?")
    print(response)
except Exception as e:
    print(f"An error occurred: {e}")