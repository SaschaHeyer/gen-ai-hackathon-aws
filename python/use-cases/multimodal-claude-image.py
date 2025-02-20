import boto3
import json
import base64

# Create a BedrockRuntime client
bedrock_runtime = boto3.client('bedrock-runtime')

# image size max 5MB
with open("kindle.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
    base64_string = encoded_string.decode('utf-8')
    
payload = {
    "modelId": "anthropic.claude-3-sonnet-20240229-v1:0",
    "contentType": "application/json",
    "accept": "application/json",
    "body": {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_string
                        }
                    },
                    {
                        "type": "text",
                        "text": """
                        Based on the image and the following product specification write a engaging product description in Dutch language.
                        
                        Display: 6.8-inch glare-free display, 300 ppi resolution
                        Storage: 8 GB or 32 GB options
                        Battery Life: Up to 10 weeks on a single charge
                        Lighting: Adjustable warm light and auto-adjusting front light
                        Waterproof: IPX8 rating, can withstand immersion in water
                        Connectivity: Wi-Fi or Wi-Fi + Free Cellular Connectivity options
                        Charging: USB-C for faster charging
                        Weight: 205 grams
                        Dimensions: 174 x 125 x 8.1 mm
                        Materials: Made with 60% post-consumer recycled plastics
                        Additional Features: Dark Mode, adjustable text size, and support for audiobooks via Bluetooth.
                        """
                    }
                ]
            }
        ]
    }
}

# Convert the payload to bytes
body_bytes = json.dumps(payload['body']).encode('utf-8')

# Invoke the model
response = bedrock_runtime.invoke_model(
    body=body_bytes,
    contentType=payload['contentType'],
    accept=payload['accept'],
    modelId=payload['modelId']
)

# Process the response
response_body = response['body'].read().decode('utf-8')
print(response_body)
