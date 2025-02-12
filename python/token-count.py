import logging
import boto3
import json
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# AWS Bedrock Model ID (Example: Claude 3 Sonnet)
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

# AWS Bedrock Pricing (per 1000 tokens)
INPUT_COST_PER_1000 = 0.003  # $0.003 per 1000 input tokens
OUTPUT_COST_PER_1000 = 0.015  # $0.015 per 1000 output tokens

# AWS Bedrock client
bedrock_client = boto3.client(service_name='bedrock-runtime')

def track_token_usage_and_cost(model_id, system_prompts, messages):
    """
    Sends a message to the Converse API, logs token usage, and calculates cost.
    """
    try:
        # Bedrock inference parameters
        inference_config = {"temperature": 0.5}
        additional_model_fields = {"top_k": 200}

        response = bedrock_client.converse(
            modelId=model_id,
            messages=messages,
            system=system_prompts,
            inferenceConfig=inference_config,
            additionalModelRequestFields=additional_model_fields
        )

        # Extract token usage
        token_usage = response.get('usage', {})
        input_tokens = token_usage.get('inputTokens', 0)
        output_tokens = token_usage.get('outputTokens', 0)
        total_tokens = token_usage.get('totalTokens', 0)

        # Calculate cost
        input_cost = (input_tokens / 1000) * INPUT_COST_PER_1000
        output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1000
        total_cost = input_cost + output_cost

        # Logging token counts and cost
        logger.info(f"Input Tokens: {input_tokens}, Cost: ${input_cost:.6f}")
        logger.info(f"Output Tokens: {output_tokens}, Cost: ${output_cost:.6f}")
        logger.info(f"Total Tokens: {total_tokens}, Total Cost: ${total_cost:.6f}")

        return {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "input_cost": round(input_cost, 6),
            "output_cost": round(output_cost, 6),
            "total_cost": round(total_cost, 6)
        }

    except ClientError as err:
        logger.error(f"AWS Client Error: {err.response['Error']['Message']}")
        return None

# Example conversation setup
system_prompts = [{"text": "You are a helpful assistant providing AI cost insights."}]
messages = [
    {"role": "user", "content": [{"text": "How much does it cost to use Claude 3 Sonnet?"}]}
]

# Track token usage and cost
token_cost_data = track_token_usage_and_cost(MODEL_ID, system_prompts, messages)

# Store the results in a JSON file
if token_cost_data:
    with open("token_usage_and_cost.json", "w") as f:
        json.dump(token_cost_data, f, indent=4)
    print("Token usage and cost saved to token_usage_and_cost.json")
