import boto3
import mimetypes

sagemaker_runtime = boto3.client("sagemaker-runtime")
endpoint_name = "bg-removal-7"

# Read the image file
with open("124079.png", "rb") as f:
    payload = f.read()

# Set the content type to multipart/form-data
content_type = "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"

# Create a multipart-form body
multipart_body = (
    "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n"
    'Content-Disposition: form-data; name="image"; filename="sample.jpg"\r\n'
    f"Content-Type: {mimetypes.guess_type('sample.jpg')[0]}\r\n\r\n"
    + payload.decode("latin1")  # Decode binary payload for multipart format
    + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--\r\n"
)

# Send the request
response = sagemaker_runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=multipart_body.encode("latin1")  # Encode back to binary
)

# Retrieve and save the response
result = response["Body"].read()
with open("output.png", "wb") as f:
    f.write(result)
