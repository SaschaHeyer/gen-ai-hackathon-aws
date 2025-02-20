import boto3
import json

# Initialize AWS Bedrock session
session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

# Load the PHP file and convert it into a text format
with open("bike.php", "r") as php_file:
    php_code = php_file.read()
    
php_as_text = f"PHP Code:\n\n{php_code}"

# Prepare the multimodal message, treating the PHP code as plain text
doc_message = {
    "role": "user",
    "content": [
        {
            "document": {
                "name": "PHP Code",
                "format": "txt",  # Transform the PHP file into a text format
                "source": {
                    "bytes": php_as_text  
                }
            }
        },
        { 
            "text": "Based on the PHP code, generate documentation for this module, including an overview, functions, code flow." 
        }
    ]
}

# Send the request to the Bedrock multimodal model
response = bedrock.converse(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    messages=[doc_message],
    inferenceConfig={
        "maxTokens": 2000,
        "temperature": 0
    },
)

# Extract and print the response
response_text = response['output']['message']['content'][0]['text']
print(response_text)
