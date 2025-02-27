import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sqs as sqs
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_event_sources as events
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3_notifications as s3_notifications
from aws_cdk import aws_dynamodb as dynamodb

from constructs import Construct

class ImageProcessingCdkStack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)


        # ✅ Create S3 Bucket with Public Access Allowed
        bucket = s3.Bucket(self, "ImageProcessingBucket",
            removal_policy=cdk.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=True,  # ✅ Enable public read access
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS  # ✅ Allow public access
        )

        # ✅ Add a Bucket Policy for Public Read
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[f"arn:aws:s3:::{bucket.bucket_name}/*"],
                principals=[iam.AnyPrincipal()]  # ✅ Allows anyone to read
            )
        )


    
        # Create SQS Queue for Image Processing
        queue = sqs.Queue(self, "ImageProcessingQueue",
            visibility_timeout=cdk.Duration.seconds(120)  # ✅ Set visibility timeout >= Lambda timeout
        )


        # Define IAM Role for Lambda
        lambda_role = iam.Role(self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonBedrockFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )

        # Create Lambda Function & Set Environment Variables
        lambda_function = _lambda.Function(self, "ProcessImageLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "SQS_QUEUE_URL": queue.queue_url,
                "RESULTS_BUCKET": bucket.bucket_name
            },
            timeout=cdk.Duration.seconds(60),  # ✅ Function timeout (should be <= visibility timeout)
            memory_size=512,
            role=lambda_role
        )

        # Set S3 to SQS Notification
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.SqsDestination(queue),
            s3.NotificationKeyFilter(suffix=".pdf")
        )

        # Set SQS to Trigger Lambda
        lambda_function.add_event_source(events.SqsEventSource(queue))

        # Grant Lambda Access to S3
        bucket.grant_read_write(lambda_function)

        table = dynamodb.Table(
            self, "DocumentProcessingResults",
            table_name="DocumentProcessingResults",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
        )

        # Grant Lambda permissions to write to DynamoDB
        table.grant_write_data(lambda_function)

        # (Optional) Explicitly attach IAM policy (if needed)
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[table.table_arn]
        ))


