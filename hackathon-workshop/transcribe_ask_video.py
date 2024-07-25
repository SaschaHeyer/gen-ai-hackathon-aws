import boto3
import time
import json
import requests

def transcribe_video(video_file_uri, job_name, region='us-west-2'):
    transcribe = boto3.client('transcribe', region_name=region)
    
    # Start the transcription job
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': video_file_uri},
        MediaFormat='mp4',
        LanguageCode='en-US'
    )
    
    # Wait for the job to complete
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Waiting for transcription job to complete...")
        time.sleep(10)
    
    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        return transcript_uri
    else:
        raise Exception("Transcription job failed")

def fetch_transcription(transcript_uri):
    response = requests.get(transcript_uri)
    transcript_data = response.json()
    return transcript_data['results']['transcripts'][0]['transcript']

def store_transcription(transcript_text, bucket_name, file_name, region='us-west-2'):
    s3 = boto3.client('s3', region_name=region)
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=transcript_text)
    return f"s3://{bucket_name}/{file_name}"

def summarize_transcription(transcript_text):
    bedrock = boto3.client(
        service_name='bedrock',
        region_name='us-west-2'
    )

    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name='us-west-2'
    )

    prompt_data = f"""you are a experienced video summarizer I provide you a transcript and you summarize it. 

    Here is the transcript of the video:
    {transcript_text}
    """

    text_gen_config = {
        "maxTokenCount": 512,
        "stopSequences": [],
        "temperature": 0,
        "topP": 0.9
    }

    body = json.dumps({
        "inputText": prompt_data,
        "textGenerationConfig": text_gen_config
    })

    model_id = 'amazon.titan-tg1-large'
    accept = 'application/json'
    content_type = 'application/json'

    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )

    response_body = json.loads(response['body'].read())
    return response_body['results'][0]['outputText']

# Example usage
video_file_uri = 's3://bedrock-doit-demo/What is AWS_ _ Amazon Web Services.mp4'
job_name = 'transcribe2'
bucket_name = 'bedrock-doit-demo'
transcription_file_name = 'transcription_2.txt'

try:
    # Transcribe video
    transcript_uri = transcribe_video(video_file_uri, job_name)
    print(f"Transcript URI: {transcript_uri}")

    # Fetch transcription
    transcript_text = fetch_transcription(transcript_uri)
    print("Transcription fetched successfully.")

    # Store transcription in S3
    stored_transcript_uri = store_transcription(transcript_text, bucket_name, transcription_file_name)
    print(f"Transcription stored at: {stored_transcript_uri}")

    # Summarize transcription
    summary = summarize_transcription(transcript_text)
    print("Summary of the video:")
    print(summary)

except Exception as e:
    print(f"An error occurred: {e}")
