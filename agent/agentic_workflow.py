from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from utils.model_loader import ModelLoader
from tools.calculator_tool import CalculatorTool

from tools.document_reader_tool import DocumentReaderTool
from tools.place_search_tool import PlaceSearchTool

# ##
# from tools.mongo_tool import mongo_query_tool
# from tools.outlook_tool import outlook_email_tool

from tools.mssql_tool import (
    mssql_query_tool,
    get_employee_login_details,
    get_employee_personal_details,
    get_unit_details,
    list_all_mssql_objects,
    get_table_columns,
)


import os
from dotenv import load_dotenv

load_dotenv()

## Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Omni-Answer"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


class GraphBuilder():
    """
    Builds a LangGraph agent with integrated tools for document reading,
    place searching, calculations, and MSSQL data access.
    """
    def __init__(self,model_provider: str = "groq"):
        
        self.model_loader = ModelLoader(model_provider=model_provider)
        self.llm = self.model_loader.load_llm()
        
        self.tools = []
        self.document_reader_tools = DocumentReaderTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        # self.mongo_tools = [mongo_query_tool]
        self.mssql_tools = [mssql_query_tool]
        # self.outlook_tools = [outlook_email_tool]
        self.mssql_tools = [
            mssql_query_tool,
            get_employee_login_details,
            get_employee_personal_details,
            get_unit_details,
            list_all_mssql_objects,
            get_table_columns
        ]
        
        self.tools.extend([
            *self.document_reader_tools.document_reader_tool_list,
            *self.calculator_tools.calculator_tool_list,
            *self.place_search_tools.search_anything_tool,
            # *self.mongo_query_tool,
            *self.mssql_tools,
            # *self.outlook_email_tool

        ])


        
        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)
        
        self.graph = None
        self.system_prompt = SYSTEM_PROMPT

    # def agent_function(self, state:MessagesState):
        """Main agent function"""
        # user_question = state["messages"]
        # # input_question = [self.system_prompt] + user_question
        # # response = self.llm_with_tools.invoke[input_question]

        # # 
        # # ✅ Inject combined document text into prompt as context
        # document_context = self.document_reader_tools.get_combined_text()

        # # ✅ System prompt now includes embedded document knowledge
        # input_question = [
        #     {"role": "system", "content": f"{self.system_prompt}\n\nContext from documents:\n{document_context}"},
        #     *user_question
        # ]
        # # 
        # response = self.llm_with_tools.invoke(input_question)
        # return{"messages":[response]}
     
     

    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_messages = state["messages"]

        # ✅ Extract past messages (full memory) and current user message
        document_context = self.document_reader_tools.get_combined_text()
        input_with_system = [
            {"role": "system", "content": f"{self.system_prompt}\n\nContext from documents:\n{document_context}"},
            *user_messages
        ]

        # 🧠 LLM sees the full memory now
        response = self.llm_with_tools.invoke(input_with_system)

        return {"messages": [*user_messages, response]}  # Preserve full memory

    

    def build_graph(self):
        ## Graph
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent",self.agent_function)
        graph_builder.add_node("tools",ToolNode(tools = self.tools))
        ## Add Edges
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent",tools_condition)
        graph_builder.add_edge("tools","agent")
        graph_builder.add_edge("agent",END)
        
        self.graph = graph_builder.compile()

        return self.graph

    def __call__(self):
        return self.build_graph()