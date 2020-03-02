import sys
import time
import os
from datetime import datetime

#this show you how you can get input
input = open(sys.argv[1]).read()

#this show if you use a python library
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

#this show you how can you run a custom library script
os.system("wget -P ./run-result " + input)

#Any files that are copied to the ./run-result folder are automatically picked up by dis.co agent, 
#and would allow you to download them as dis.co results later on in any of the client libraries, 
#or the Web UI.the content inside the run-result will be downloaded back as a zip file.
