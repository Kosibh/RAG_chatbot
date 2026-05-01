## Importing Packages ##
import os
import re
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile

from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders import UnstructuredPowerPointLoader

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

from functions import chunk_data, calculate_embedding_cost, create_embeddings

#--------------------------------------------------------------------------------------------#

load_dotenv()

# Getting OpenAI API key from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

#--------------------------------------------------------------------------------------------#

app = FastAPI()

#--------------------------------------------------------------------------------------------#

# Initialize global state
vector_store = None

# Initialize a variable to track the number of chunks
num_chunks = 0

# Keep the chunks for embedding cost calculation
processed_chunks = [] 

#--------------------------------------------------------------------------------------------#

# Endpoint to process files, chunk, and calculate embeddings
@app.post("/upload-files/")
async def upload_files(files: List[UploadFile]):
    global vector_store, num_chunks, processed_chunks

    all_documents = []
    
    # Save and process files
    for file in files:
        file_path = os.path.join("tempDir", file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        if file.filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file.filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file.filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding='UTF-8')
        elif file.filename.endswith(".pptx"):
            loader = UnstructuredPowerPointLoader(file_path)
        elif file.filename.endswith(".xlsx"):
            loader = UnstructuredExcelLoader(file_path)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        documents = loader.load()
        all_documents.extend(documents)
        
    # Chunk data
    chunks = chunk_data(all_documents)
    num_chunks = len(chunks)
    processed_chunks = chunks
    
    # Calculate embedding cost
    tokens, embedding_cost = calculate_embedding_cost(chunks)
    
    # Create embeddings and save them in FAISS vector store
    vector_store = create_embeddings(chunks)
    
    # Return the number of chunks and the embedding cost
    return {"num_chunks": num_chunks, "embedding_cost": embedding_cost}

#--------------------------------------------------------------------------------------------#

# Endpoint to process URLs, chunk, and calculate embeddings
class URLInput(BaseModel):
    urls: List[str]

@app.post("/process-urls/")
async def process_urls(url_input: URLInput):
    global vector_store, num_chunks, processed_chunks

    urls = url_input.urls
    if len(urls) > 5:
        raise HTTPException(status_code=400, detail="You can only process up to 5 URLs at a time.")
    
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    # Chunk data
    chunks = chunk_data(data)
    num_chunks = len(chunks)
    processed_chunks = chunks
    
    # Calculate embedding cost
    tokens, embedding_cost = calculate_embedding_cost(chunks)
    
    # Create embeddings and save them in FAISS vector store
    vector_store = create_embeddings(chunks)
    
    # Return the number of chunks and the embedding cost
    return {"num_chunks": num_chunks, "embedding_cost": embedding_cost}

#--------------------------------------------------------------------------------------------#

# Endpoint to generate a response based on the user's query
class QueryRequest(BaseModel):
    query: str

@app.post("/generate-response/")
async def generate_response(query_request: QueryRequest):
    global vector_store, num_chunks, processed_chunks

    if vector_store is None:
        raise HTTPException(status_code=400, detail="Please upload and process your data (vector store is not created)")

    # generating response with source file reference
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 10})
    chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    ans = chain({"question": query_request.query})

    # response text cleaning
    ans['sources'] = ans['sources'].lstrip('./').lstrip('tempDir\\')
    ans['answer'] = re.sub(r'\s*SOURCES:$','', ans['answer'])

    return {
            "answer": ans['answer'],
            "sources": ans['sources'],
           }

