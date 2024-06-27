from typing import TypedDict, Annotated,Literal

from agents.agent import (
   Agent
)
from prompts.prompts import (
    agent_system_prompt_template

)
from langgraph.graph import StateGraph, END
from utils.helper_functions import extract_docker_error_steps
import json
import ast
from tools.docker_builder import execute_docker_cmds
# from tools.google_serper import get_google_serper
# from tools.basic_scraper import scrape_website
from states.state import AgentGraphState, get_agent_graph_state, state

from langgraph.checkpoint.sqlite import SqliteSaver
from agents.docker_agent import DockerAgent



class DockerGraph():
    def __init__(self,server,model,stop,tools):
        self.agent = DockerAgent(tools=tools,server=server, model=model, stop=stop)
        
        graph=StateGraph(AgentGraphState)
        graph.add_node("agent",self.agent.run_agent)
        graph.add_node("action",self.agent.execute_tools)
        graph.add_node("parser",self.agent.parse_output)
        graph.set_entry_point("agent")
        graph.add_conditional_edges("agent",self.agent.should_continue, {"continue":"action","end":END})
        graph.add_edge('action','parser')
        graph.add_edge('parser','agent')

        self.dockergraph= graph

def compile_workflow(graph):
    db_location="/home/pranay/persistance.db"
    memory =SqliteSaver.from_conn_string(db_location)
    workflow = graph.compile(checkpointer=memory)
    return workflow
