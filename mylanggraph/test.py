import subprocess

process = subprocess.Popen("docker build -t im1 .", shell=True,stderr=subprocess.PIPE,cwd="fastApi")

        # Provide the sudo password
sudo_password = b'AppsTek@123\n'  # Add '\n' at the end to simulate pressing Enter

# Communicate with the process and provide the sudo password
output, error = process.communicate()
print(output,"output", error,"error")
