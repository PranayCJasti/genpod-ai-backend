from agents.agent import Agent
from states.state import AgentGraphState, get_agent_graph_state, state
from utils.helper_functions import extract_docker_error_steps
from typing import TypedDict, Annotated,Literal
import ast
from states.state import AgentGraphState



class DockerAgent():
    def __init__(self, tools, server, model, stop):
        self.agent= Agent(tools=tools,model_service=server, model_name=model, stop=stop)
    def should_continue(self, data:AgentGraphState) -> Literal["__end__","action"]:
        if data['agent_outcome']['tool_choice']=='no_tool' or data['agent_outcome']['error_correction'] != 'none':
            return "end"
        else:
            return "continue"

    def run_agent(self, data:AgentGraphState):
        print("agent data",data)
        agent_outcome=self.agent.think(data)
        chatHis=data['chat_history']
        chatHis.append(data['input'])
        return {"agent_outcome": agent_outcome}
    #agent work after think think
    def execute_tools(self,data:AgentGraphState):
        agent_action=data['agent_outcome']
        output=self.agent.work(agent_action)
        
        print(f"The agent action is {agent_action}")
        print(f"The tool result is: {output}")
        return {"intermediate_steps": [(agent_action, str(output))]}

    def parse_output(self,data:AgentGraphState):
        print("tool output",data["intermediate_steps"][-1][1])
        tool_output=ast.literal_eval(data['intermediate_steps'][-1][1])
        parsed_output=' '.join(str(e) for e in extract_docker_error_steps(tool_output))
        print(f"the parsed output {parsed_output}")
        return {"latest_execution_result":parsed_output}





