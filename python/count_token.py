from anthropic_bedrock import AnthropicBedrock

client = AnthropicBedrock()
prompt = "Hello, world!"
token_count = client.count_tokens(prompt)
print(token_count)