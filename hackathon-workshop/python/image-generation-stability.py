from botocore.config import Config
from botocore.exceptions import ClientError
import json
from PIL import Image
from io import BytesIO
import base64
from base64 import b64encode
from base64 import b64decode
import boto3


#Create the connection to Bedrock

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2', 
    
)

bedrock = boto3.client(
    service_name='bedrock',
    region_name='us-west-2', 
    
)

# Let's see all available Stability Models
available_models = bedrock.list_foundation_models()

for model in available_models['modelSummaries']:
  if 'stability' in model['modelId']:
    print(model)


# Define prompt and model parameters
prompt_data = """young man waling on a green frozen lake on a snowy day"""

body = json.dumps({"text_prompts":[{"text":prompt_data}],
  "cfg_scale":6,
  "seed":10,
  "steps":50}) 

modelId = 'stability.stable-diffusion-xl-v1'
accept = 'application/json'
contentType = 'application/json'

response = bedrock_runtime.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
response = json.loads(response.get('body').read())
images = response.get('artifacts')

image = Image.open(BytesIO(b64decode(images[0].get('base64'))))
image.save("generated/generated_image.png")