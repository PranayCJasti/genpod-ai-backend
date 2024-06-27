from utils.command_enum import DockerCommand
from pydantic_class.docker_builder_classs import DockerImageBuilder
from utils.helper_functions import run_root_cmds
from pydantic import validate_call,Field
# imageName:str ,action:DockerCommand,pathToDockerfile:str
# 
@validate_call
def execute_docker_cmds(imageName:str ,action:DockerCommand,pathToDockerfile:str) -> dict:
    """
    Execute run or build commands as requested by the agent by following the user prompts 
    
    Parameters:
    imageName(str): A string containing the name of the docker image from the user input
    action(DockerCommand): A object of type DockerCommand Enum which will have just the docker action needs to be performed
    pathToDockerfile(str): A string containing the path to the folder where the dockerfile  or the image is located if provided by the user or else it is empty string
   
    Returns:
    dict: The output of the command execution
    """
    # docker_builder = DockerImageBuilder(**kwargs)
   
    cmd_exe=["sudo -S docker build -t %s ." ,"sudo -S docker run %s"]
    
    cmd_output={"execution":False}
    cmd_output['command']=action
    print(action.value,"action")
    if(action.value =="build"):
        i=cmd_exe[0]
        cmd_output["execution"]=True
    elif (action.value=="run"):
        i=cmd_exe[1]
        cmd_output["execution"]=True
    else:
        return cmd_output
    
    result=run_root_cmds(i % imageName,pathToDockerfile)
    print("result",result)
    # print(result.stderr=="")
    if ("Output" in result):
        cmd_output["result"]=result.replace('Output:',"")
    else:
        cmd_output["error"]=result.replace('Error:',"") 

    return cmd_output
   

