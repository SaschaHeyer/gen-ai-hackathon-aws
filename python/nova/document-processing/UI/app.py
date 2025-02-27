import streamlit as st
import boto3
import json

# AWS Configuration
AWS_REGION = "us-west-2"
DYNAMODB_TABLE = "DocumentProcessingResults"
S3_BUCKET = "imageprocessingcdkstack-imageprocessingbucket2c60f-pub1fy82segn"

# Amazon Nova Lite pricing (USD per 1,000 tokens)
PRICE_INPUT_TOKEN = 0.00006  # $0.00006 per token → $0.06 per 1,000 tokens
PRICE_OUTPUT_TOKEN = 0.000015  # $0.000015 per token → $0.015 per 1,000 tokens

# Initialize AWS Clients
dynamodb = boto3.client("dynamodb", region_name=AWS_REGION)

# 🚀 Function to Fetch Processed Documents from DynamoDB
def fetch_processed_documents():
    try:
        response = dynamodb.scan(TableName=DYNAMODB_TABLE)
        return response.get("Items", [])
    except Exception as e:
        st.error(f"⚠️ Error fetching records from DynamoDB: {e}")
        return []

# 🚀 Function to Get JSON Data from Public S3 URL
def fetch_json_from_s3(json_url):
    try:
        response = boto3.client("s3").get_object(
            Bucket=S3_BUCKET, Key=json_url.replace(f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/", "")
        )
        return json.loads(response["Body"].read().decode("utf-8"))
    except Exception as e:
        st.error(f"⚠️ Error reading JSON file: {e}")
        return None

# 🚀 Function to Convert String Tokens to Integer
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

# 🚀 Function to Calculate Token Costs
def calculate_total_cost(documents):
    total_input_tokens = sum(safe_int(doc.get("input_tokens", {}).get("N", 0)) for doc in documents)
    total_output_tokens = sum(safe_int(doc.get("output_tokens", {}).get("N", 0)) for doc in documents)
    total_tokens = total_input_tokens + total_output_tokens

    # Cost calculation (dividing by 1000 to get per 1,000 tokens)
    cost_input = (total_input_tokens / 1000) * PRICE_INPUT_TOKEN
    cost_output = (total_output_tokens / 1000) * PRICE_OUTPUT_TOKEN
    total_cost = cost_input + cost_output

    return total_input_tokens, total_output_tokens, total_tokens, total_cost

# 🎨 Streamlit UI
st.set_page_config(layout="wide")  # ✅ Full-width mode
st.title("📄 AI Document Processing Dashboard")
st.write("View extracted data, token usage, and PDFs from processed documents.")

# Fetch all documents
documents = fetch_processed_documents()

if not documents:
    st.warning("⚠️ No processed documents found in DynamoDB.")
else:
    # 📊 **Display total token usage and cost**
    st.markdown("## 📊 Token Usage Overview")
    total_input_tokens, total_output_tokens, total_tokens, total_cost = calculate_total_cost(documents)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🔹 Input Tokens", f"{total_input_tokens:,}")
    col2.metric("🔹 Output Tokens", f"{total_output_tokens:,}")
    col3.metric("⚡ Total Tokens", f"{total_tokens:,}")
    col4.metric("💰 Estimated Cost (USD)", f"${total_cost:.6f}")

    # **Display each processed document**
    st.markdown("## 📂 Processed Documents")

    for doc in documents:
        st.divider()
        st.subheader(f"📂 Processed Document: `{doc['id']['S']}`")

        # Extract file paths
        input_file = doc["input_file"]["S"].replace(f"s3://{S3_BUCKET}/", "").strip()
        output_file = doc["output_file"]["S"].replace(f"s3://{S3_BUCKET}/", "").strip()

        # Construct public URLs
        pdf_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{input_file}"
        json_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{output_file}"

        # 🔹 Create Two-Column Layout (Left: PDF, Right: JSON)
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader("📑 PDF Preview")
            st.markdown(f"[📄 Open PDF in Browser]({pdf_url})")
            st.markdown(f'<iframe src="{pdf_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True)

        with col2:
            st.subheader("📊 Extracted Information")
            json_data = fetch_json_from_s3(json_url)
            if json_data:
                st.json(json_data)
            else:
                st.warning("⚠️ Extracted JSON file not found.")

        # 📌 **Token details per document**
        st.markdown("### 🔢 Token Details")
        col1, col2, col3 = st.columns(3)
        col1.metric("🔹 Input Tokens", f"{safe_int(doc.get('input_tokens', {}).get('N', 0)):,}")
        col2.metric("🔹 Output Tokens", f"{safe_int(doc.get('output_tokens', {}).get('N', 0)):,}")
        col3.metric("⚡ Total Tokens", f"{safe_int(doc.get('input_tokens', {}).get('N', 0)) + safe_int(doc.get('output_tokens', {}).get('N', 0)):,}")

st.divider()
st.success("✅ Dashboard Loaded Successfully!")
