import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel

role = "arn:aws:iam::303673948954:role/sascha-sagemaker"  # Replace with your IAM role for SageMaker


# Hub Model configuration. https://huggingface.co/models
hub = {
	'HF_MODEL_ID':'google/siglip-base-patch16-224',
	'HF_TASK':'zero-shot-image-classification'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	transformers_version='4.37.0',
	pytorch_version='2.1.0',
	py_version='py310',
	env=hub,
	role=role,
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1, # number of instances
	instance_type='ml.m5.xlarge' # ec2 instance type
)
