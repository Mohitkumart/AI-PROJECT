from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os
from agent.agentic_workflow import GraphBuilder

import traceback
import sys
from typing import List, Optional

app = FastAPI()

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

        # Build graph and get app
        graph = GraphBuilder(model_provider='groq')
        react_app = graph()

        # Save graph visualization (optional)
        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png", "wb") as f:
            f.write(png_graph)
        print(f"✅ Graph saved at {os.getcwd()}")

        # Properly format message
        # messages = [{"role": "user", "content": querry.question}]

        # Invoke agent with valid message format---------
        # output = react_app.invoke({"messages": messages})

        #------memory
        messages = querry.memory or []
        messages.append({"role": "user", "content": querry.question})

        output = react_app.invoke({"messages": messages})
        #----------

        print(f"🧪 Output type: {type(output)}")
        print(f"🧪 Output content: {output}")

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
