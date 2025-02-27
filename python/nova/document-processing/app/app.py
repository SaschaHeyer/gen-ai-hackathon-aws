import aws_cdk as cdk
from image_processing_cdk_stack import ImageProcessingCdkStack

app = cdk.App()

env = cdk.Environment(account="303673948954", region="us-west-2")

ImageProcessingCdkStack(app, "ImageProcessingCdkStack", env=env)

app.synth()
