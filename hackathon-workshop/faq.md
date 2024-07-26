## Error: The security token included in the request is invalid.
Verify AWS CLI Configuration: Make sure your AWS CLI is correctly configured and can successfully make requests.

````
aws sts get-caller-identity
````

If this is also running into errors this could be caused by switching wlans can cause issues with the AWS session.

Run the following again

````
aws configure
````

alternative
If switching from temporary IAM role credentials to IAM user credentials, ensure AWS_SESSION_TOKEN, which is only used for temporary credentials, is no longer set:

````
unset AWS_SESSION_TOKEN # unset environment variable
````

## Converse API vs Invoke API

https://aws.amazon.com/about-aws/whats-new/2024/05/amazon-bedrock-new-converse-api

On May 30th, Amazon Bedrock announced the new Converse API, which provides a consistent way for developers to invoke Amazon Bedrock models and manage multi-turn conversations. This API simplifies the process by removing the need to adjust for model-specific differences and enabling structured conversational history. Additionally, it supports Tool use (function calling) for select models, allowing developers to access external tools and APIs, expanding the capabilities of their applications.

To use the Converse API, you must use the following Amazon Bedrock models:
https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html

