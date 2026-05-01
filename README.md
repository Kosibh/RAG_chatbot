# RAG Chatbot 
An AI-powered Retrieval-Augmented Generation (RAG) chatbot that allows users to query documents and receive intelligent responses using LLMs.

## Features

- **FastAPI**: To build backend for handling requests.
- **Streamlit**: To create chat-like user interface (frontend).
- **LangChain**: For document ingestion, chunking, and text embeddings.
- **OpenAI GPT-3.5**: For language model processing and generating responses.
- **FAISS**: For Semantic search, vector storage to store and retrieve embeddings.
- **Python-dotenv**: To manage environment variables securely.

## Tech Stack

- Python
- FastAPI
- Streamlit
- LangChain
- OpenAI API
- FAISS

## My Contributions

- Set up and debugged the full-stack project locally
- Cleaned and restructured the repository
- Improved backend–frontend workflow
- Prepared system for enhancements

## Setup Instructions

1. Install Anaconda on your system.
2. Download the code on your system and open new anaconda terminal in the parent dir of the downloaded code.
3. Create a new virtual env using below command. <br>
**-> conda create -n chatbotenv python=3.8**
4. Now activate the virtual env, by using below command. <br>
**-> conda activate chatbotenv**
5. Now, install the required packages in the above virtual env. <br>
**-> pip install -r requirements.txt**
6. Now open a new terminal/cmd in the parent dir of the code and run below command <br>
**-> cd backend**
7. Now run the backend application by using below commands. <br>
**-> uvicorn app:app --reload**
8. Now again open a new terminal/cmd in the parent dir of the code and run below command <br>
**-> cd frontend**
9. Now run the backend application by using below commands. <br>
**-> streamlit run main.py**
10. Now, app should be up and running on local port 8501, to view the app goto your browser and paste the below URL. <br>
**-> http://localhost:8501/**

