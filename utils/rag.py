from typing import List

def query_rag_agent(question: str, vectorstore, agent):
    """
    Retrieve top-k relevant chunks from the vectorstore and pass them to the agent.
    """
    # ✅ Retrieve top-k chunks from vector DB based on semantic similarity
    docs = vectorstore.similarity_search(question, k=4)
    retrieved_context = "\n\n".join([doc.page_content for doc in docs])

    # ✅ Inject context into prompt for the agent
    messages = [
        {"role": "system", "content": "Use the following context to answer the user's question."},
        {"role": "user", "content": f"{retrieved_context}\n\nQuestion: {question}"}
    ]

    return agent.invoke({"messages": messages})