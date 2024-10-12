from ultralytics import YOLO
import torch

import os
import sys
import time
from dataclasses import dataclass

from brain_tumor_detection.exception import CustomException
from brain_tumor_detection.logger import logging

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
SOURCE_PATH = os.path.dirname(SCRIPT_PATH)
PROJECT_PATH = os.path.dirname(SOURCE_PATH)
DATA_BASE = os.path.dirname(PROJECT_PATH)

@dataclass
class ModelTrainerConfig:
    data_path=os.path.join(DATA_BASE, '../data/TumorDetectionYolov8/brainTumorDetection/data.yaml')
    
@dataclass
class YOLOV8TrainerConfig:
    epochs = 50
    imgsz=640
    patience = 20
    optimizer = 'auto'
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        self.yolov8trainer_config = YOLOV8TrainerConfig()
        
    def getGPU(self):
        if torch.cuda.device_count() > 0:
            return list(range(torch.cuda.device_count()))
        else:
            return 'cpu'
            
    def yolov8Train(self):
        try:
            start_time = time.time()
            logging.info("Start training")
            
            model = YOLO("yolov8n.yaml")  # build a new model from YAML
            model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)
            model = YOLO("yolov8n.yaml").load("yolov8n.pt")  # build from YAML and transfer weights
            
            device = self.getGPU()

            results = model.train(data=self.model_trainer_config.data_path, 
                            epochs=self.yolov8trainer_config.epochs, 
                            imgsz=self.yolov8trainer_config.imgsz, 
                            patience=self.yolov8trainer_config.patience,
                            optimizer=self.yolov8trainer_config.optimizer,
                            device=device)
           
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            logging.info("%s", results)
            logging.info(f"Finish training, total time usage: {elapsed_time:.6f} second.")
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == '__main__':
    modelTrainer = ModelTrainer()
    modelTrainer.yolov8Train()
