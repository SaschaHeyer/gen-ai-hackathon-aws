import json
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

role = "arn:aws:iam::303673948954:role/sascha-sagemaker"  # Replace <account-id> with your AWS account ID


hub = {
	'HF_MODEL_ID':'meta-llama/Llama-3.1-8B',
	'SM_NUM_GPUS': json.dumps(1),
	'HUGGING_FACE_HUB_TOKEN': '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'
}

# create Hugging Face Model Class
huggingface_model = HuggingFaceModel(
	image_uri=get_huggingface_llm_image_uri("huggingface",version="2.2.0"),
	env=hub,
	role=role, 
)

# deploy model to SageMaker Inference
predictor = huggingface_model.deploy(
	initial_instance_count=1,
	instance_type="ml.g5.2xlarge",
	container_startup_health_check_timeout=300,
 endpoint_name="llama318b"
  )
  
# send request
predictor.predict({
	"inputs": "My name is Clara and I am",
})