from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import sys

if __name__=='__main__':
    try:
        pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(pipeline_config_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config_obj)
        logger.info("Initate Data Ingestion")
        data_ingestion_artifact = data_ingestion_obj.initate_data_ingestion()
        print(data_ingestion_artifact)
        data_validation_config_obj = DataValidationConfig(pipeline_config_obj)
        data_validation_obj = DataValidation(data_validation_config_obj,data_ingestion_artifact)
        data_validation_artifact = data_validation_obj.initate_data_validation()
        data_transformation_config_obj = DataTransformationConfig(pipeline_config_obj)
        data_transformation_obj = DataTransformation(data_transformation_config_obj,data_validation_artifact)
        data_transformation_artifact = data_transformation_obj.initate_data_transformation()
        model_trainer_config_obj = ModelTrainerConfig(pipeline_config_obj)
        model_trainer_obj = ModelTrainer(model_trainer_config_obj,data_transformation_artifact)
        model_trainer_artifact = model_trainer_obj.initate_model_trainer()
        print(model_trainer_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)