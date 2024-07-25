require 'aws-sdk-bedrockruntime'  # Ensure you have this gem installed
require 'json'

# Initialize the Bedrock client using the default configuration
client = Aws::BedrockRuntime::Client.new(
  region: 'us-west-2'  # Specified region
)

# Define the parameters for the invoke_model method
params = {
  model_id: 'amazon.titan-tg1-large',  # Model ID
  body: {
    inputText: "Hello, Bedrock!"
  }.to_json
}

# Call the Bedrock API
begin
  response = client.invoke_model(params)
  body = response.body.read
  result = JSON.parse(body)
  puts "Response: #{result}"
rescue Aws::BedrockRuntime::Errors::ServiceError => e
  puts "Error: #{e.message}"
end
