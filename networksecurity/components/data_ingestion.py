from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys
import os
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self)->pd.DataFrame:
        try:
            self.database = self.data_ingestion_config.database_name
            self.collection = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
            self.collection = self.mongo_client[self.database][self.collection]
            
            # return (self.database,self.collection,self.mongo_client)
            df = pd.DataFrame(list(self.collection.find()))
            # return df.columns
            if '_id' in df.columns:
                df.drop(columns=["_id"],inplace=True)
            
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def export_dataframe_as_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_file_path,index=False)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def split_data_train_test(self,dataframe):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logger.info("Exported Train and Test data")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_dataframe_as_feature_store(dataframe=dataframe)
            self.split_data_train_test(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,tested_file_path=self.data_ingestion_config.testing_file_path)

            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
