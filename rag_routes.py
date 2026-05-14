from fastapi import APIRouter

from app.rag import (
    model,
    collection
    
)

router = APIRouter()


@router.post("/rag/index-document")
def index_document(pdf_path: str):

    text = extract_text(pdf_path)

    chunks = chunk_text(text)

    embeddings = create_embeddings(chunks)

    store_embeddings(chunks, embeddings)

    return {
        "message": "Document indexed successfully"
    }


@router.post("/rag/search")
def semantic_search(query: str):

    embedding_model = load_model()

    query_embedding = embedding_model.encode(query)

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=5
    )

    return results