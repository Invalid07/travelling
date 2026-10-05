import os 
import operator
from typing import TypedDict , Annotated

import psycopg
from langgraph.graph import StateGraph , START ,END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import AnyMessage , HumanMessage , SystemMessage ,AIMessage 
from langgraph.checkpoint.postgres import PostgresSaver

from langchain_groq import ChatGroq

# tools
from tools.tevaily_tool import tavily_search
from tools.flight_tool import search_flight

# dotenv 
from dotenv import load_dotenv 
load_dotenv()

# db_url
DB_url=os.getenv("db_url")

# llm model
llm = ChatGroq(model= "openai/gpt-oss-20b" )

# ------------langgraph--------------------

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage],operator.add]
    user_query: str
    flight_results :str
    hotel_results :str
    itinerary :str
    llm_calls:int


def flight_agent (state:AgentState):
    query=state["user_query"]
    flight_data=search_flight(query)
    return {
            "flight_results":flight_data,
            "messages":[AIMessage(content=f"Flight search results for query ")],
            "llm_calls":state.get("llm_calls",0)+1
            }

def hotel_agent (state:AgentState):
    query = state["user_query"]
    hotel_data = tavily_search(query)
    return {
            "hotel_results":hotel_data,
            "messages":[AIMessage(content=f"Hotel search results for query ")],
            "llm_calls":state.get("llm_calls",0)+1
            }
    


