from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish
import operator

from typing import TypedDict, Annotated, List, Union,Literal


# Define the state object for the agent graph
class AgentGraphState(TypedDict):
    input:str
    chat_history: List[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[List[tuple[AgentAction, str]], operator.add]
    latest_execution_result: str
    # docker_agent_response:Annotated[list,add_messages]
    # main_agent_response:Annotated[list,add_messages]


# Define the nodes in the agent graph
def get_agent_graph_state(state:AgentGraphState, state_key:str):
    if state_key == "docker_agent_all":
        return state["docker_agent_response"]
    elif state_key == "docker_agent_latest":
        if state["docker_agent_response"]:
            return state["docker_agent_response"][-1]
        else:
            return state["docker_agent_response"]
    # elif state_key=="main_agent_all":
    #     return state["main_agent_response"]
    # elif state_key=="main_agent_latest":
    #     if state["main_agent_response"]:
    #         return state["main_agent_response"][-1]
    #     else:
    #         return state["main_agent_response"]        
    else:
        return None
    
state = {
    "input":"",
    "chat_history": [],
    "agent_outcome": None,
    "intermediate_steps":[],
    "latest_execution_result":""
    # "docker_agent_response":[],
    # "main_agent_response":[]
}