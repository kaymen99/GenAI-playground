import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from langchain_pinecone import PineconeVectorStore
from src.utils import download_hugging_face_embeddings
from src.graph import Workflow


# load all env variables
load_dotenv()

# create fask app instance
app = Flask(__name__)

# Get pinecone API keys
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# Index name
index_name = "research-assistant"

# Get the embeddings model
embeddings = download_hugging_face_embeddings("sentence-transformers/all-MiniLM-L6-v2")
 
# load previously stored Pinecone index
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
docs_retriever = docsearch.as_retriever()

# Build RAG graph worfklow
rag_graph = Workflow(docs_retriever).app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    question = request.form["question"]
    inputs = {"question": question}
    print("Question: ", question)
    for output in rag_graph.stream(inputs):
        for key, value in output.items():
            print(f"Finished running: {key}")
    answer = value["generation"]
    print("Answer:", answer)
    return str(answer)

if __name__ == "__main__":
    app.run(port="8080", debug=True)