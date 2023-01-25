import subprocess
from subprocess import CREATE_NEW_CONSOLE

subprocess.Popen("python process.py -f process1.txt -i 1", creationflags=CREATE_NEW_CONSOLE)
subprocess.Popen("python process.py -f process2.txt -i 2", creationflags=CREATE_NEW_CONSOLE)
