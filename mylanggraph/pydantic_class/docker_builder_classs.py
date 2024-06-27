from pydantic import BaseModel, Field
from utils.command_enum import DockerCommand
class DockerImageBuilder(BaseModel):
    imageName:str = Field(description="Name of the docker image from the user input")
    action:DockerCommand=Field(description="Type of the action needs to perform given by the agent")
    pathToDockerfile:str=Field(..., description="This is the path to the folder where the dockerfile  or the image is located if provided by the user or else it is empty string")
    class Config:
        arbitrary_types_allowed = True