import boto3

client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
)
MODEL_ID = "us.amazon.nova-pro-v1:0"

with open('documents/2.pdf', "rb") as file:
    doc_bytes = file.read()

messages =[
    {
    "role": "user",
    "content": [
        {
            "document": {
                "format": "pdf",
                "name": "DocumentPDFmessages",
                "source": {
                    "bytes": doc_bytes
                }
            }
        },
        {
            "text": """
            You are a entity extraction specialist. 
            You MUST answer in JSON format only. Please follow the output schema below.

            Output Schema:

            {
                "type": "object",
                "properties": {
                    "invoice_number": {
                        "type": "string"
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {
                                    "type": "string"
                                },
                                "quantity": {
                                    "type": "string"
                                },
                                "total": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                }
            }
"""
        }
    ]
}

]

model_parameter = {"temperature": 0.3}

model_response = client.converse(
    modelId=MODEL_ID, 
    messages=messages, 
    inferenceConfig=model_parameter)

print(model_response['output']['message']['content'][0]['text'])