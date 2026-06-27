from app.ingestion import load_and_split
from app.vectorstore import create_vectorstore
from app.rag_pipeline import build_rag

def run_chatbot(file_path):
    docs = load_and_split(file_path)
    vectorstore = create_vectorstore(docs)
    qa_chain = build_rag(vectorstore)
    return qa_chain