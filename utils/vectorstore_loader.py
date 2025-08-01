import os
from langchain.docstore.document import Document
import pickle

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings



# Set where vectorstore will be saved
VECTORSTORE_DIR = "vectorstore"
VECTORSTORE_INDEX_FILE = os.path.join(VECTORSTORE_DIR, "index.faiss")
VECTORSTORE_PKL_FILE = os.path.join(VECTORSTORE_DIR, "index.pkl")

# ✅ Create vectorstore from plain text
def create_vectorstore_from_text(text: str) -> FAISS:
    if not os.path.exists(VECTORSTORE_DIR):
        os.makedirs(VECTORSTORE_DIR)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Split text into chunks by paragraph (or add chunking logic)
    chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
    docs = [Document(page_content=chunk) for chunk in chunks]

    vectorstore = FAISS.from_documents(docs, embedding=embeddings)

    # ✅ Save FAISS index + metadata
    vectorstore.save_local(VECTORSTORE_DIR)
    return vectorstore

# ✅ Check if vectorstore is already saved
def vectorstore_exists() -> bool:
    return os.path.exists(VECTORSTORE_INDEX_FILE) and os.path.exists(VECTORSTORE_PKL_FILE)

# ✅ Load previously saved vectorstore
def load_vectorstore() -> FAISS:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(VECTORSTORE_DIR, embeddings, allow_dangerous_deserialization=True)
