# Object Detection in dis.co

This code uses the ImageAI python library to perform object detection in images. 
Since object recognition is an embarrassingly parallel task, we can use dis.co to get our object detection results faster

## Prerequisites
1. A dis.co account
2. A local python installation
3. The disco python package installed
4. Logged into the disco cli

## Running the demo
1. Add the custom docker image "iqoqo/runtime:full-py37-cpu" to your disco account through the web UI
2. Get the ID of your custom docker image by running 
`disco docker list`
3. Create & run your job in dis.co 
`disco job create --name "Object Recognition Demo" --script FirstObjectDetection.py --input mewithmug.jpg --constants "requirements.txt" --docker-image-id <your_docker_image_ID> --run`

##What's happening

