require 'bundler/setup'
require 'sinatra'
require 'aws-sdk-bedrockruntime'
require 'json'


# Initialize the Bedrock client using the default configuration
client = Aws::BedrockRuntime::Client.new(region: 'us-west-2')

get '/' do
  erb :index
end

post '/invoke' do
  input_text = params[:input_text]

  # Define the parameters for the invoke_model method
  params = {
    model_id: 'amazon.titan-tg1-large',  # Model ID
    body: {
      inputText: input_text
    }.to_json
  }

  # Call the Bedrock API
  begin
    response = client.invoke_model(params)
    body = response.body.read
    result = JSON.parse(body)
    @result = result.to_json
  rescue Aws::BedrockRuntime::Errors::ServiceError => e
    @error = e.message
  end

  erb :result
end

__END__

@@index
<!DOCTYPE html>
<html>
<head>
  <title>Bedrock API POC</title>
</head>
<body>
  <h1>Invoke Bedrock API</h1>
  <form action="/invoke" method="post">
    <label for="input_text">Input Text:</label>
    <input type="text" id="input_text" name="input_text">
    <input type="submit" value="Invoke">
  </form>
</body>
</html>

@@result
<!DOCTYPE html>
<html>
<head>
  <title>Bedrock API POC</title>
</head>
<body>
  <h1>Result</h1>
  <% if @result %>
    <pre><%= @result %></pre>
  <% else %>
    <p>Error: <%= @error %></p>
  <% end %>
  <a href="/">Back</a>
</body>
</html>
