import boto3 
import requests
from requests_aws4auth import AWS4Auth 
import pprint

session = boto3.Session(region_name='us-west-2')

credentials = session.get_credentials()

model_id = "amazon.titan-tg1-large" #change depending on your model of choice

endpoint = f'https://bedrock-runtime.us-west-2.amazonaws.com/model/{model_id}/invoke'

payload = {
  'inputText': 'What can I do in Berlin?',
  'textGenerationConfig': {
    'maxTokenCount': 512,
    'stopSequences': [],
    'temperature': 0,
    'topP': 0.9
  } 
}

signer = AWS4Auth(credentials.access_key,  
                   credentials.secret_key,
                   'us-west-2', 'bedrock') 
                   
response = requests.post(endpoint, json=payload, auth=signer)

print(response.text)


response_json = response.json()

# Access the outputText field
output_text = response_json['results'][0]['outputText']

# Pretty print the outputText
pprint.pprint(output_text)