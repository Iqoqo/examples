#note: please replace raymondlo84 with your own docker id

#build the docker image, will take a while and this requires internet connection.
docker build -t raymondlo84/disco_python_sdk -f disco.dockerfile .

#run the docker image to verify it works locally
#docker run -it raymondlo84/disco_python_sdk:latest

#push this to the repository (change this to your own path)
#docker push raymondlo84/disco_python_sdk:latest

