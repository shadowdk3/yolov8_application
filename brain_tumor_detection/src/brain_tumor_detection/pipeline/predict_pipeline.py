import sys
import time
import os
import cv2

import numpy as np

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors

from brain_tumor_detection.exception import CustomException
from brain_tumor_detection.logger import logging

import matplotlib.pyplot as plt

class PredictPipeline:
    def __init__(self):
        model_path = 'brain_tumor_detection/runs/detect/train/weights/best.pt'
        
        self.model = YOLO(model_path)

    def normalize_image(self, image):
        return image / 255.0

    def resize_image(self, image, size=(640, 640)):
        return cv2.resize(image, size)

    def predict(self, filepath):
        try:
            start_time = time.time()

            if os.path.isdir(filepath):
                image_files = [file for file in os.listdir(filepath) if file.endswith('.jpg')]

                if len(image_files) > 0:
                    num_images = len(image_files)
                    step_size = max(1, num_images // 9)
                    selected_images = [image_files[i] for i in range(0, num_images, step_size)]
        
                    fig, axes = plt.subplots(3, 3, figsize=(20, 21))
                    fig.suptitle('TEST Set Inferences', fontsize=24)

                    for i, ax in enumerate(axes.flatten()):
                        if i < len(selected_images):
                            image_path = os.path.join(filepath, selected_images[i])
                            image = cv2.imread(image_path)
                            
                            if image is not None:
                                resized_image = self.resize_image(image, size=(640, 640))
                                normalized_image = self.normalize_image(resized_image)
                                normalized_image_uint8 = (normalized_image * 255).astype(np.uint8)
                                
                                results = self.model.predict(source=normalized_image_uint8, imgsz=640, conf=0.5)
                                
                                annotated_image = results[0].plot(line_width=1)
                                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                                
                                ax.imshow(annotated_image_rgb)
                            else:
                                logging.info(f"Failed to load image {image_path}")
                                raise CustomException(e, sys)
                            
                        ax.axis('off')

                    plt.tight_layout()
                    plt.savefig('multi.jpg')
                    plt.show()
            
            else:
                image_files = filepath
                
                image = cv2.imread(image_files)
                # original_height, original_width = image.shape[:2] 
                
                resized_image = self.resize_image(image, size=(640, 640))
                normalized_image = self.normalize_image(resized_image)
                normalized_image_uint8 = (normalized_image * 255).astype(np.uint8)
                                
                results = self.model.predict(source=normalized_image_uint8, imgsz=640, conf=0.5)

                annotated_image = results[0].plot(line_width=1)
                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

                # reshaped_image = cv2.resize(annotated_image_rgb, (original_width, original_height))
                
                return (
                    True, 
                    annotated_image_rgb
                )
                # cv2.imwrite('single.jpg', annotated_image_rgb)
                
        except Exception as e:
            raise CustomException(e, sys)
        
# if __name__ == "__main__":
#     predictPipeline = PredictPipeline()
#     predictPipeline.predict('../data/TumorDetectionYolov8/brainTumorDetection/test/images')
#     predictPipeline.predict('../data/TumorDetectionYolov8/brainTumorDetection/test/images/volume_268_slice_46_jpg.rf.f35fba1c4ee98c30a98d21c7959f1089.jpg')
