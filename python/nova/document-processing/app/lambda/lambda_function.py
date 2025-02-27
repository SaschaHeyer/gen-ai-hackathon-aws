import json
import boto3
import os
import urllib.parse
import uuid
from datetime import datetime

# Initialize AWS clients
s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")
dynamodb = boto3.resource("dynamodb")  
table = dynamodb.Table("DocumentProcessingResults")

# Environment Variables
SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]
RESULTS_BUCKET = os.environ["RESULTS_BUCKET"]
MODEL_ID = "us.amazon.nova-pro-v1:0"

def lambda_handler(event, context):
    """
    AWS Lambda function triggered by SQS to process PDF documents.
    Downloads from S3, sends to Bedrock Nova, stores JSON back in S3, and logs to DynamoDB.
    """
    print("🔹 Received event:", json.dumps(event, indent=2))

    for record in event["Records"]:
        try:
            s3_bucket, s3_key = None, None

            # ✅ Extract S3 event from SQS message
            if "body" in record:
                body = json.loads(record["body"])  # Convert 'body' string to JSON
                if "Records" in body and len(body["Records"]) > 0:
                    s3_event = body["Records"][0]  # Extract the first S3 event
                    s3_bucket = s3_event["s3"]["bucket"]["name"]
                    s3_key = s3_event["s3"]["object"]["key"]

            # ✅ Validate extracted values
            if not s3_bucket or not s3_key:
                print("[ERROR] Missing 's3_bucket' or 's3_key' in event:", record)
                continue  # Skip processing if missing

            s3_key = urllib.parse.unquote_plus(s3_key)

            print(f"✅ Processing file: s3://{s3_bucket}/{s3_key}")
            print(f"🔹 Attempting to download file from S3: s3://{s3_bucket}/{s3_key}")

            # ✅ Step 1: Download PDF from S3
            pdf_obj = s3_client.get_object(Bucket=s3_bucket, Key=s3_key)
            pdf_bytes = pdf_obj["Body"].read()

            print("✅ Successfully downloaded PDF file")

            # ✅ Step 2: Call AWS Bedrock Nova for PDF processing
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "document": {
                                "format": "pdf",
                                "name": "DocumentPDFmessages",
                                "source": {
                                    "bytes": pdf_bytes  # ✅ Use raw bytes
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

            response = bedrock_client.converse(
                modelId=MODEL_ID, messages=messages, inferenceConfig={"temperature": 0.3}
            )

            print("✅ Bedrock API Response:", json.dumps(response, indent=2))  # Log Full Response

            # ✅ Step 3: Handle Bedrock response safely
            try:
                response_text = response["output"]["message"]["content"][0]["text"]
                extracted_data = json.loads(response_text)  # Ensure valid JSON
            except (KeyError, json.JSONDecodeError) as e:
                print(f"[ERROR] Failed to parse Bedrock response: {e}")
                extracted_data = {"error": "Invalid response from Bedrock"}

            # ✅ Step 4: Extract token usage details
            token_usage = response.get("usage", {})
            input_tokens = token_usage.get("inputTokens", 0)
            output_tokens = token_usage.get("outputTokens", 0)
            total_tokens = token_usage.get("totalTokens", 0)

            # ✅ Step 5: Save JSON output to S3
            json_filename = s3_key.replace(".pdf", ".json")
            json_key = f"results/{json_filename}"

            s3_client.put_object(
                Bucket=RESULTS_BUCKET,
                Key=json_key,
                Body=json.dumps(extracted_data, indent=2),
                ContentType="application/json"
            )

            print(f"✅ Stored results in s3://{RESULTS_BUCKET}/{json_key}")

            # ✅ Step 6: Store metadata & token usage in DynamoDB
            item = {
                "id": str(uuid.uuid4()),  # ✅ Unique ID for DynamoDB entry
                "input_file": f"s3://{s3_bucket}/{s3_key}",
                "output_file": f"s3://{RESULTS_BUCKET}/{json_key}",
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "processed_at": datetime.utcnow().isoformat(),
            }

            table.put_item(Item=item)
            print(f"✅ Stored metadata & token usage in DynamoDB: {json.dumps(item, indent=2)}")

        except Exception as e:
            print(f"[ERROR] Failed to process record: {e}")
            continue

    return {"statusCode": 200, "body": "Processing completed"}
