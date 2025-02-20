require 'nokogiri'

# Function to clean HTML content and ensure proper spacing
def extract_text_from_html(html_content)
  # Parse the HTML content
  document = Nokogiri::HTML(html_content)

  # Extract text with improved whitespace handling
  text = document.search('//text()').map(&:text).join(' ')
                .gsub(/\s+/, ' ').strip # Normalize whitespace

  return text
end

# Example HTML content
html_content = '<html><head><title>Example</title></head><body><h1>Hello World!</h1><p>This is an <a href="#">example</a> paragraph.</p></body></html>'

# Get clean text
plain_text = extract_text_from_html(html_content)
puts plain_text
