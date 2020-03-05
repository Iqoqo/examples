from imageai.Detection import ObjectDetection
import os
# import requests
import urllib.request


if __name__ == "__main__":
    if not os.path.exists('run-result'):
        os.mkdir('run-result')

    yolo_url = "https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5"
    urllib.request.urlretrieve(yolo_url, 'yolo_weights_file')

    execution_path = os.getcwd()

    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    # detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath( os.path.join(execution_path , "yolo_weights_file"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "mewithmug.jpg"), output_image_path=os.path.join(execution_path ,"run-result/mewithmugnew2.jpg"), minimum_percentage_probability=30)

    for eachObject in detections:
        print(eachObject["name"] , " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
        print("--------------------------------")
