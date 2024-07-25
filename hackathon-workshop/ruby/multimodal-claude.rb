require 'aws-sdk-bedrockruntime'
require 'json'
require 'base64'

# Initialize the Bedrock client using default configuration
client = Aws::BedrockRuntime::Client.new(
  region: 'us-west-2'
)

# Encode the image file to base64
encoded_string = ''
File.open("../files/london.jpg", "rb") do |image_file|
  encoded_string = Base64.strict_encode64(image_file.read)
end

# Define the payload
payload = {
  modelId: "anthropic.claude-3-sonnet-20240229-v1:0",
  contentType: "application/json",
  accept: "application/json",
  body: {
    anthropic_version: "bedrock-2023-05-31",
    max_tokens: 1000,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: "image/png",
              data: encoded_string
            }
          },
          {
            type: "text",
            text: "Write me a detailed description of this photo"
          }
        ]
      }
    ]
  }.to_json
}

# Call the Bedrock API
begin
  response = client.invoke_model(
    body: payload[:body],
    content_type: payload[:contentType],
    accept: payload[:accept],
    model_id: payload[:modelId]
  )
  response_body = JSON.parse(response.body.read)
  puts "Response: #{response_body}"
rescue Aws::BedrockRuntime::Errors::ServiceError => e
  puts "Error: #{e.message}"
end
