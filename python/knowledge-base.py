import boto3
agentruntime_client = boto3.client('bedrock-agent-runtime')
question = "tell me something about apohis?"
kb_config = {"knowledgeBaseId":"G5OS6LDWEN", "modelArn":"arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"}
response = agentruntime_client.retrieve_and_generate( input={'text': question},retrieveAndGenerateConfiguration={"type":"KNOWLEDGE_BASE", 'knowledgeBaseConfiguration':kb_config})

citations = response.get('citations', [])
for citation in citations:
    
    
    text_response = citation.get('generatedResponsePart', {}).get('textResponsePart', {}).get('text', "")
    references = citation.get('retrievedReferences', [])

    # Printing the extracted text response
    print("\nText Response:\n")
    print(text_response)

    # Printing the citation (reference)
    print("\nCitations:\n")
    for ref in references:
        ref_text = ref.get('content', {}).get('text', "")
        ref_location = ref.get('location', {}).get('s3Location', {}).get('uri', "")
        print(f"Reference Text: {ref_text}")
        print(f"Source: {ref_location}\n")
