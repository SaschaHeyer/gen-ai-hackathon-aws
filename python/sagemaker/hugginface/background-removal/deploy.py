import sagemaker

sess = sagemaker.Session()
role = "arn:aws:iam::303673948954:role/sascha-sagemaker"  # Replace with your IAM role for SageMaker

custom_image_uri = "303673948954.dkr.ecr.us-west-2.amazonaws.com/background-removal-inference-image-2:latest"


from sagemaker.model import Model

# Define the model with the custom image URI
bg_removal_model = Model(
    role=role,
    image_uri=custom_image_uri,
    sagemaker_session=sess
)

# Deploy the model to an endpoint
instance_type = "ml.g4dn.xlarge"  # Choose an instance that supports GPU if needed
bg_removal_endpoint = bg_removal_model.deploy(
    initial_instance_count=1,
    instance_type=instance_type,
    endpoint_name="bg-removal-7"
)
