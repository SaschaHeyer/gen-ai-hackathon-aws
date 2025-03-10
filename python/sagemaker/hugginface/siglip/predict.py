import boto3
import json
import base64
from PIL import Image
import requests
import io

# Initialize SageMaker runtime client
sagemaker_runtime = boto3.client("sagemaker-runtime")

# Replace with your actual endpoint name
endpoint_name = "huggingface-pytorch-inference-2025-03-10-13-50-55-897"

# Load and preprocess the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Test with an example image from COCO dataset
image_url = "http://images.cocodataset.org/val2017/000000039769.jpg"
response = requests.get(image_url)
image = Image.open(io.BytesIO(response.content))

# Save and encode the image
image_path = "test_image.jpg"
image.save(image_path)
base64_image = encode_image(image_path)

# Define candidate labels
candidate_labels = ["a cat", "a dog", "a car"]

# Create the JSON payload
payload = {
    "inputs": base64_image,
    "parameters": {"candidate_labels": candidate_labels}
}

# Invoke the SageMaker endpoint
response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="application/json",
    Body=json.dumps(payload),
)

# Parse the response
result = json.loads(response["Body"].read().decode("utf-8"))
print(result)
