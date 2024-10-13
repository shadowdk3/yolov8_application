import matplotlib.pyplot as plt
from PIL import Image
import os
from ultralytics import YOLO
import cv2
import numpy as np
import sys

from medical_instance_segmentation.exception import CustomException
from medical_instance_segmentation.logger import logging

class PredictPipeline:
    def __init__(self):
        model_path = 'medical_stance_segmentation/HuBMAP/yolov8x-seg/weights/best.pt'
        
        self.model = YOLO(model_path)
        
    def normalize_image(self, image):
        return image / 255.0

    def resize_image(self, image, size=(640, 640)):
        return cv2.resize(image, size)

    def predict(self, filepath):
        try:
            image = cv2.imread(filepath)
            
            resized_image = self.resize_image(image, size=(640, 640))
            normalized_image = self.normalize_image(resized_image)
            normalized_image_uint8 = (normalized_image * 255).astype(np.uint8)

            results = self.model.predict(source=normalized_image_uint8, imgsz=640, conf=0.5)

            annotated_image = results[0].plot(line_width=1)
            annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                
            # plt.imshow(annotated_image_rgb) 
            # plt.show() 

            return (
                True, 
                annotated_image_rgb
            )
            
        except Exception as e:
            raise CustomException(e, sys)

# if __name__ == "__main__":
#     predictPipeline = PredictPipeline()
#     predictPipeline.predict('dataset/val/images/dc03d69afd95.tif')
