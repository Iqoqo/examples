# Example code for Running Dis.co's Python SDK with Custom Docker Images

This code demonstrate how we can run a job with Dis.co's Python SDK + a custom docker image.

The code got two parts.

1. The Dis.co SDK demo code
2. The custom docker build files and scripts

To build the docker image, you can run the script provided.

To test the solution, you have to first setup the docker image on the dis.co account, and set it as the default. 

Then, you can run the main.py afterwards with the customized features provided in the docker (i.e., using an external library in this case)

Before you start, we recommend that you setup a new virtual environment with Python

```
python3 -m venv venv
source venv/bin/activate
``` 

# How to run

1. Install Dis.co SDK. 
```
pip3 install disco --upgrade

```

2. Run the docker build script (for the first time only)
```
./build_docker.sh
```
3. Upload and Setup the Docker Image on Dis.co 


Follow the instruction here, and push your docker image up according.
```
https://docs.docker.com/docker-hub/repos/
```

And follow the instruction here to get your docker image setup on Dis.co

```
https://docs.dis.co/integrations/custom-docker-images
```

4. Run the Job
```
python3 main.py
```

This will prompt a selection on which Docker image to run on. Make sure you select the correct one or it won't run.

5. Check the results.
We download the result back on the current directory. You should be able to see two new jpg files =)




