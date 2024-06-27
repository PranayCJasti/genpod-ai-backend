from agent_graph.graph import  compile_workflow
from tools.docker_builder import execute_docker_cmds
from models.openai_models import OpenAIModel
from models.ollama_models import OllamaModel
from agent_graph.graph import DockerGraph

# server = 'ollama'
# model = 'llama3:instruct'
# model_endpoint = None
# 
tools = [execute_docker_cmds]
model_service = OpenAIModel
model_name = 'gpt-3.5-turbo'
stop = None
# model_service = OllamaModel
# model_name = 'llama3'
# stop = "<|eot_id|>"

# server = 'vllm'
# model = 'meta-llama/Meta-Llama-3-70B-Instruct' # full HF path
# model_endpoint = 'https://kcpqoqtjz0ufjw-8000.proxy.runpod.net/' 
# #model_endpoint = runpod_endpoint + 'v1/chat/completions'
# stop = "<|end_of_text|>"

iterations = 5

print ("Creating graph and compiling workflow...")
graph = DockerGraph(server=model_service, model=model_name, stop=stop,tools=tools)
workflow = compile_workflow(graph.dockergraph)
print ("Graph and workflow created.")


if __name__ == "__main__":

    verbose = False
    inputs={"input": "",
        "latest_execution_result":""}

    while True:
        query = input("Please enter your research question: ")
        if query.lower() == "exit":
            break
        # print(inputs)
        inputs['input']=query
        dict_inputs = inputs
        thread = {"configurable": {"thread_id": "4"}}
        limit = {"recursion_limit": iterations}
        for event in workflow.stream( dict_inputs, thread , stream_mode="values"):
            for k,v  in event.items():
                if k != "__end__":
                    print("\n")

           
        



    # Uncoment below to run with OpenAI
  

    # Uncomment below to run with Ollama
    # model_service = OllamaModel
    # model_name = 'llama3'
    # stop = "<|eot_id|>"

    # agent = Agent(tools=tools, model_service=model_service, model_name=model_name, stop=stop)

    # while True:
    #     prompt = input("Ask me anything: ")
    #     if prompt.lower() == "exit":
    #         break
    #     # agent.test()
    #     agent.work(agent.think(prompt))



    