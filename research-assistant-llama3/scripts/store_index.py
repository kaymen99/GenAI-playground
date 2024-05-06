import os
from dotenv import load_dotenv
from src.utils import load_pdf, text_splitter, download_hugging_face_embeddings, create_index_and_store_vectors_to_pinecone

load_dotenv()

# Get pinecone API keys
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')

# Index name
index_name = "research-assistant"

# extract data from pdf the "papers" folder
data = load_pdf("../papers")

# get the data text chunks
text_chunks = text_splitter(data)

# Download embeddings model
embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings_dimension = 384 # From huggingFace model description
embeddings = download_hugging_face_embeddings(embeddings_model_name)

# Create index and store embeddings into Pinecone
create_index_and_store_vectors_to_pinecone(
    index_name,
    text_chunks,
    embeddings,
    embeddings_dimension,
    PINECONE_API_KEY
)