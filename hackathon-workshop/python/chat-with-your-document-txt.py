import boto3, json

session = boto3.Session()
bedrock = session.client(service_name='bedrock-runtime')

with open("/Users/sascha/Desktop/development/gen-ai-hackathon-aws/hackathon-workshop/files/purebrew_manual.txt", "rb") as doc_file:
    doc_bytes = doc_file.read()

doc_message = {
    "role": "user",
    "content": [
        {
            "document": {
                "name": "Document 1",
                "format": "txt",
                "source": {
                    "bytes": doc_bytes 
                }
            }
        },
        { "text": "Based on the document, how can I clean the coffee machine?" }
    ]
}

response = bedrock.converse(
    modelId="anthropic.claude-3-sonnet-20240229-v1:0",
    messages=[doc_message],
    inferenceConfig={
        "maxTokens": 2000,
        "temperature": 0
    },
)

response_text = response['output']['message']['content'][0]['text']
print(response_text)
