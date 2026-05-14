from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader
import uuid

model = None

def load_model():

    global model

    if model is None:
        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return model

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="financial_docs"
)

def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        text += page.extract_text()

    return text


def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunks.append(text[i:i+chunk_size])

    return chunks



def create_embeddings(chunks):

    embedding_model = load_model()

    embeddings = embedding_model.encode(chunks)

    return embeddings



def store_embeddings(chunks, embeddings):

    for i, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk],
            embeddings=[embeddings[i].tolist()],
            ids=[str(uuid.uuid4())]
        )

        