from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import os

from agent.agentic_workflow import GraphBuilder

app = FastAPI()

class QuerryRequest(BaseModel):
    question : str
    

@app.get("/query")
async def querry_travel_agent(querry:QuerryRequest):
    try:
        print(querry)
        graph = GraphBuilder(model_provider='groq')
        react_app = graph()

        png_graph = react_app.get_graph().draw_mermaid_png()
        with open("my_graph.png","wb") as f:
            f.write(png_graph)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()}")

        # Assuming request is a pydamic object like {"question" : "your text"}
        messages = {"messages": {querry.question}}
        output = react_app.invoke(messages)

        # if result is dict with messages
        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content  ## Get Last AI rersponse
        else:
            final_output = str[output]
        
        return {"answer" : final_output}


    except Exception as e:
        return JSONResponse(status_code = 500, content = {"error": str(e)})
        

