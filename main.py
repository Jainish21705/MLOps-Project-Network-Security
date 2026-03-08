from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import sys

if __name__=='__main__':
    try:
        pipeline_config_obj = TrainingPipelineConfig()
        data_ingestion_config_obj = DataIngestionConfig(pipeline_config_obj)
        data_ingestion_obj = DataIngestion(data_ingestion_config_obj)
        logger.info("Initate Data Ingestion")
        artifact = data_ingestion_obj.initate_data_ingestion()
        print(artifact)
    except Exception as e:
        raise NetworkSecurityException(e,sys)