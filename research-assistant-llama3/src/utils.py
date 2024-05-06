from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from scidownl import scihub_download
import pinecone, requests


# extract titles of research papers related to given topic
# using semanticscholar api
def get_papers_titles(topic, papers_count):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/autocomplete"
    params = {
        "query": topic,
        "limit": papers_count  
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        titles = [paper['title'] for paper in data['matches']]
        return titles
    else:
        print("Failed to fetch data from Semantic Scholar API")
        return []


def download_multi_papers(sources):
    """Example of downloading multiple papers fro Scihub.
    All papers will be downloaded to the ./paper/ directory,
    and their filenames are the paper titles.
    """
    for title in sources:
        print("Downloading papers...")
        scihub_download(title, paper_type='title', out="./papers/")


def load_pdf(path):
    loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def text_splitter(data):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
    text_chunks = splitter.split_documents(data)
    return text_chunks

def download_hugging_face_embeddings(model):
    print("Downloading Embeddings model from HF....")
    embeddings = HuggingFaceEmbeddings(model_name=model)
    return embeddings

def create_index_and_store_vectors_to_pinecone(index_name, text_chunks, embeddings, dimension, api_key):
    # Create Pinecone index
    pc = pinecone.Pinecone(api_key=api_key)
    pc.create_index(
        name=index_name,
        dimension=dimension,
        metric="cosine",
        spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1")
    )

    # Create data embeddings for each chunk and store vectors into Pinecone
    docsearch = PineconeVectorStore.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)

    return docsearch
