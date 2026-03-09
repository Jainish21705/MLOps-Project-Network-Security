import sys
import os
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config_obj = DataIngestionConfig(self.training_pipeline_config)
            logger.info("Start the Data Ingestion")
            data_ingestion_obj = DataIngestion(self.data_ingestion_config_obj)
            data_ingestion_artifact = data_ingestion_obj.initate_data_ingestion()
            logger.info("Data Ingestion Compeleted")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact):
        try:
            self.data_validation_config_obj = DataValidationConfig(self.training_pipeline_config)
            logger.info("Start the Data Validation")
            data_validation_obj = DataValidation(self.data_validation_config_obj,data_ingestion_artifact)
            data_validation_artifact = data_validation_obj.initate_data_validation()
            logger.info("Data Validation Compeleted")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact):
        try:
            self.data_transformation_config_obj = DataTransformationConfig(self.training_pipeline_config)
            logger.info("Start the Data Transformation")
            data_transformation_obj = DataTransformation(self.data_transformation_config_obj,data_validation_artifact)
            data_transformation_artifact = data_transformation_obj.initate_data_transformation()
            logger.info("Data Transformation Compeleted")
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact):
        try:
            self.model_trainer_config_obj = ModelTrainerConfig(self.training_pipeline_config)
            logger.info("Start the Model Trainer")
            model_trainer_obj = ModelTrainer(self.model_trainer_config_obj,data_transformation_artifact)
            model_trainer_artifact = model_trainer_obj.initate_model_trainer()
            logger.info("Model Trainer Compeleted")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
