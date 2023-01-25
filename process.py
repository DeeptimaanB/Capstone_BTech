import subprocess
from subprocess import CREATE_NEW_CONSOLE
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--instance", dest="instance", help="Instance Number")
parser.add_argument("-f", "--filename", dest="filename", help="Filename")

options = parser.parse_args()

stri="INPUT//"+str(options.filename)

with open(stri,"r") as file:
    data=file.readlines()
    for exe in data:
        code = 1
        while(code==1):
            exe=exe.rstrip("\n")
            pro = subprocess.Popen(exe, creationflags=CREATE_NEW_CONSOLE)
            code = pro.wait()
            if(code==1):
                print(exe+" FAILED - Process "+str(options.instance))
            if(code==0):
                print(exe+" COMPLETED - Process "+str(options.instance))
            
