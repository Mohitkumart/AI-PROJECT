from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
from agent.agentic_workflow import GraphBuilder

import traceback
import sys
from typing import List, Optional

from tools.document_reader_tool import DocumentReaderTool
from utils.vectorstore_loader import create_vectorstore_from_text
import hashlib 

app = FastAPI()

from utils.vectorstore_loader import (
    create_vectorstore_from_text,
    load_vectorstore,
    vectorstore_exists
)


#  Helper: compute hash of combined document content
def compute_hash(text: str) -> str:  # 
    return hashlib.md5(text.encode()).hexdigest()  # 

# Global vectorstore
vectorstore = None
doc_hash_file = "vectorstore/doc_hash.txt"  # ✅ For tracking document changes


# ------------------------------------------------------------------
# ✅ New hash-based smart vectorstore loader
def compute_doc_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

@app.on_event("startup")
def startup_event():
    global vectorstore

    reader = DocumentReaderTool()
    text = reader.get_combined_text()
    current_hash = compute_doc_hash(text)

    saved_hash = ""
    if os.path.exists(doc_hash_file):
        with open(doc_hash_file, "r") as f:
            saved_hash = f.read().strip()

    if saved_hash != current_hash or not vectorstore_exists():
        print("🆕 New or changed documents found. Recreating vectorstore...")
        vectorstore = create_vectorstore_from_text(text)
        with open(doc_hash_file, "w") as f:
            f.write(current_hash)
        print("✅ Vectorstore recreated and saved.")
    else:
        print("✅ No document changes. Loading existing vectorstore...")
        vectorstore = load_vectorstore()
# ------------------------------------------------------------------


# class QuerryRequest(BaseModel):
#     question: str

# for adding memory
class QuerryRequest(BaseModel):
    question: str
    memory: Optional[List[dict]] = []  # 🧠 Added memory field


@app.post("/querry")
async def querry_travel_agent(querry: QuerryRequest):
    try:
        print(f"📥 Received question: {querry.question}")

        global vectorstore  # reuse shared vectorstore loaded at startup

        # Build graph and get app
        graph = GraphBuilder(model_provider='groq')
        react_app = graph()
        

        # Save graph visualization (optional)
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        # print(f"✅ Graph saved at {os.getcwd()}")

        # # 📄 Load documents & vectorstore
        # reader = DocumentReaderTool()
        # combined_text = reader.get_combined_text()
        # vectorstore = create_vectorstore_from_text(combined_text)

        # Properly format message
        # messages = [{"role": "user", "content": querry.question}]

        # Invoke agent with valid message format---------
        # output = react_app.invoke({"messages": messages})

        #------memory
        messages = querry.memory or []
        messages.append({"role": "user", "content": querry.question})

        # Inject context from document search
        relevant_docs = vectorstore.similarity_search(querry.question, k=3)  # ✅ Top 3 matching chunks
        context = "\n\n".join([doc.page_content for doc in relevant_docs])  # ✅ Merge text chunks
        messages.insert(0, {
            "role": "system",
            "content": f"Use this context:\n{context}"  # ✅ Inject retrieved doc content
        })

        #  Invoke the agent with message + RAG context
        output = react_app.invoke({"messages": messages})
        #----------

        # print(f"🧪 Output type: {type(output)}")
        # print(f"🧪 Output content: {output}")

        # Extract response
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        # Advanced traceback logging
        exc_type, exc_value, exc_tb = sys.exc_info()
        tb = traceback.extract_tb(exc_tb)
        last_call = tb[-1]
        error_location = f"{last_call.filename}, line {last_call.lineno}, in {last_call.name}"
        error_message = f"{type(e).__name__}: {str(e)} at {error_location}"

        print(f"❌ Exception occurred: {error_message}")
        return JSONResponse(status_code=500, content={"error": error_message})
