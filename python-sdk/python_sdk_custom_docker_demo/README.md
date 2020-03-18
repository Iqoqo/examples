# Running Dis.co's Python SDK with Custom Docker Images

This example code demonstrates how to use Dis.co's Python SDK + a custom docker image.

The example code consists of two parts.

1. The source code 
	- main.py - Python SDK usage code
	- server.py - Server side Python script 
	- task[1-2].txt - Data(task) files
2. The custom docker build files and scripts to build such. 

# Install

Before you start, we recommend that you setup a new virtual environment with Python

```
#create the virtual environment
python3 -m venv venv 
#activate the virtual environment
source venv/bin/activate
``` 

Then, install Dis.co's Python SDK + CLI with the following command line.

```
pip3 install disco --upgrade
```

# Usage

1. Run the docker build script (for the first time only)

	```
	./build_docker.sh
	```

2. Upload and Setup the Docker Image on Dis.co 

	Follow the instruction here, and push your docker image up according.
	```
	https://docs.docker.com/docker-hub/repos/
	```

	And follow the instruction here to get your docker image setup on Dis.co

	```
	https://docs.dis.co/integrations/custom-docker-images
	```

3. Run the Job

	```
	python3 main.py
	```

	This will prompt a selection on which Docker image to run on. Make sure you select the correct one or it won't run.

4. Check the results.

	The code downloads the result back on the current directory. You should be able to see two new jpg files on your local current directory. 
