from fastapi import APIRouter, UploadFile, File, Form, Depends
import shutil
import os
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Document

router = APIRouter()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/documents/upload")
def upload_document(
    title: str = Form(...),
    company_name: str = Form(...),
    document_type: str = Form(...),
    uploaded_by: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    os.makedirs("uploaded_docs", exist_ok=True)

    file_location = f"uploaded_docs/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_document = Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        uploaded_by=uploaded_by,
        file_path=file_location
    )

    db.add(new_document)

    db.commit()

    return {
        "message": "Document uploaded successfully"
    }

@router.get("/documents")
def get_documents(db: Session = Depends(get_db)):

    documents = db.query(Document).all()

    return documents


@router.get("/documents/{document_id}")
def get_single_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    return document


@router.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        return {
            "error": "Document not found"
        }

    db.delete(document)

    db.commit()

    return {
        "message": "Document deleted"
    }