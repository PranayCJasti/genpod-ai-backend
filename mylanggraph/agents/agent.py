from prompts.prompts import agent_system_prompt_template
from models.openai_models import OpenAIModel
from models.ollama_models import OllamaModel
from tools.docker_builder import execute_docker_cmds
from toolbox.toolbox import ToolBox
from states.state import AgentGraphState

class Agent:
    def __init__(self, tools, model_service, model_name, stop=None):
        """
        Initializes the agent with a list of tools and a model.

        Parameters:
        tools (list): List of tool functions.
        model_service (class): The model service class with a generate_text method.
        model_name (str): The name of the model to use.
        """
        # self.state=state
        self.tools = tools
        self.model_service = model_service
        self.model_name = model_name
        self.stop = stop
        self.tool_description= self.prepare_tools()
    
    def update_state(self, key, value):
        self.state = {**self.state, key: value}

    def prepare_tools(self):
        """
        Stores the tools in the toolbox and returns their descriptions.

        Returns:
        str: Descriptions of the tools stored in the toolbox.
        """
        toolbox = ToolBox()
        toolbox.store(self.tools)
        tool_descriptions = toolbox.tools()
        return tool_descriptions

    def think(self, state):
        """
        Runs the generate_text method on the model using the system prompt template and tool descriptions.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        dict: The response from the model as a dictionary.
        """
        # tool_descriptions = self.prepare_tools()
        agent_system_prompt = agent_system_prompt_template.format(tool_descriptions=self.tool_description,chat_history='$$ '.join(str(e) for e in state['chat_history'][-5:]))

        # Create an instance of the model service with the system prompt

        if self.model_service == OllamaModel:
            print("ollama")
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0,
                stop=self.stop
            )
        else:
            model_instance = self.model_service(
                model=self.model_name,
                system_prompt=agent_system_prompt,
                temperature=0
            )
        # prompt= state['input'] 
        if state['latest_execution_result'] != '':
            prompt="User asigned task :"+state['input']+ 'This is the output from the tool execution '+state['latest_execution_result']+ " Now that you have details about the task and the execution output, check if you can complete the task  "
        else:
            prompt= state['input'] 
            # prompt="User asigned task :"+state['input']+'/n'+ 'This is the output from the tool execution '+state['latest_execution_result']
        print("PROMPT",prompt)
        # Generate and return the response dictionary
        agent_response_dict = model_instance.generate_text(prompt)
        print(agent_response_dict)
        return agent_response_dict

    def work(self, agent_response_dict):
        """
        Parses the dictionary returned from think and executes the appropriate tool.

        Parameters:
        prompt (str): The user query to generate a response for.

        Returns:
        The response from executing the appropriate tool or the tool_input if no matching tool is found.
        """
        # agent_response_dict = self.think(prompt)
        tool_choice = agent_response_dict.get("tool_choice")
        tool_input = agent_response_dict.get("tool_input")

        for tool in self.tools:
            if tool.__name__ == tool_choice:
                response = tool(**tool_input)

                print(response)
                return response
                # return tool(tool_input)

        print(tool_input)
        
        return 
    

    def test(self):
        for tool in self.tools:
            if tool.__name__ == "execute_docker_cmds":
                response = tool(*{'imageName': 'i', 'action': 'abc', 'pathToDockerfile': ''})

                print(response)
                return
        return


# Example usage
# if __name__ == "__main__":

#     tools = [execute_docker_cmds]


#     # Uncoment below to run with OpenAI
#     # model_service = OpenAIModel
#     # model_name = 'gpt-3.5-turbo'
#     # stop = None

#     # Uncomment below to run with Ollama
#     model_service = OllamaModel
#     model_name = 'llama3'
#     stop = "<|eot_id|>"

#     agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop)

#     # while True:
#     #     prompt = input("Ask me anything: ")
#     #     if prompt.lower() == "exit":
#     #         break
#     #     # agent.test()
#     #     agent.work(agent.think(prompt))
