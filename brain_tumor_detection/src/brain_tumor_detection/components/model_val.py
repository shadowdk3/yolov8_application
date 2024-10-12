from ultralytics import YOLO
import torch

import pandas as pd

import os
import sys
import time
from dataclasses import dataclass

from src.exception import CustomException
from src.logger import logging

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.dirname(SCRIPT_PATH)
PROJECT_PATH = os.path.dirname(SOURCE_PATH)

@dataclass
class ModelValConfig:
    model_path = 'runs/detect/train/weights/best.pt'

class ModelVal:
    def __init__(self):
        self.model_val_config = ModelValConfig()
            
    def yolov8Val(self):
        try:
            start_time = time.time()
            
            best_model = YOLO(self.model_val_config.model_path)
            metrics = best_model.val(split='val')
            metrics = pd.DataFrame.from_dict(metrics.results_dict, orient='index', columns=['Metric Value'])
           
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            hours, rem = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(rem, 60)

            logging.info(f"Elapsed time: {hours}:{minutes}:{seconds}")

            logging.info("%s", metrics)
            
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':
    modelVal = ModelVal()
    modelVal.yolov8Val()
