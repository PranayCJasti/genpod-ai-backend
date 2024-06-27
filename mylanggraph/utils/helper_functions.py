import subprocess
import re
import os
from utils.get_keys import load_config

config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'config.yaml')
load_config(config_path)
def run_root_cmds(cmd:str,Cwd:str):
    print(cmd, Cwd)
    try:
        process = subprocess.Popen(cmd, shell=True,stdin=subprocess.PIPE,stderr=subprocess.PIPE,cwd=Cwd)

        print("passsword")
        # Provide the sudo password
        sudo_password = os.getenv('SUDO_KEY')+'\n' # Add '\n' at the end to simulate pressing Enter
        print("passsword",sudo_password) 
        # Communicate with the process and provide the sudo password
        output, error = process.communicate(input= sudo_password.encode())
        print(output,"output", error,"error")
        if process.returncode != 0:
        # print(error.decode())
            return "Error: " +error.decode()
        else:
            # print("Output:",error.decode())
            return "Output: "+error.decode()
    except FileNotFoundError:
        return "Error: There is no file in the specified location check the path provided path"+Cwd 
    except Exception as e:
        return "Error: "+repr(e)
    



def extract_docker_error_steps(output):
    if(output['execution']==True):
        if( 'error' in  output.keys()):
            step_pattern = re.compile(r'(#\d+ \[.*?\].*?(?=#\d+ \[|$))', re.DOTALL)
            error_pattern = re.compile(r'ERROR: (.+)')
            steps = step_pattern.findall(output['error'])
            error_steps = [step for step in steps if error_pattern.search(step)]
            if error_steps:
                return error_steps
            else:
                return [output['error']]
        else:
            return [ output['command']+" :Command executed successfully"]
    else:
        return [output['command']+ " :Command not found, you are only allowed to use build or run"]