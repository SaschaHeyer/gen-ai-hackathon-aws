from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
import boto3

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("/Users/sascha/Desktop/development/gen-ai-hackathon-aws/hackathon-workshop/files/bedrock-api.pdf")
api_pages = loader.load_and_split()

loader = PyPDFLoader("/Users/sascha/Desktop/development/gen-ai-hackathon-aws/hackathon-workshop/files/bedrock-api.pdf")
ug_pages = loader.load_and_split()

import json
bedrockruntime = boto3.client('bedrock-runtime')
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrockruntime)

from langchain.vectorstores import chroma
bigvectorstore_chroma = chroma.Chroma.from_documents(
    api_pages+ug_pages,
    bedrock_embeddings
)

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

prompt_template = """

Human: Use the following pieces of context to provide an accurate answer to the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

<context>
{context}
</context

Question: {question}

Assistant:"""


# - create the Anthropic Model
llm = Bedrock(model_id="anthropic.claude-v2", client=bedrockruntime, model_kwargs={'max_tokens_to_sample':1024})
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=bigvectorstore_chroma.as_retriever(
        search_type="similarity", search_kwargs={"k": 5}
    ),
    return_source_documents=False,
    chain_type_kwargs={"prompt": PROMPT},
    verbose = True
)

query = """How to invoke a bedrock model with boto3? Provide a concrete example"""
result = qa({"query": query})

print(result)