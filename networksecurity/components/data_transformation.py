from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.constants import training_pipeline
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_obj,read_data
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
import os
import sys
import pickle

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_transformer_object(cls):
        try:
            imputer = KNNImputer(**training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor = Pipeline(
                steps= [("imputer",imputer)]
            )
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def initate_data_transformation(self):
        try:
            # Read the validated train and test file 
            train_df = read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = read_data(self.data_validation_artifact.valid_test_file_path)
            
            # Dropping the target column from the dataframe
            input_feature_train_df = train_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            target_feature_train_df = train_df[training_pipeline.TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            input_feature_test_df = test_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            target_feature_test_df = test_df[training_pipeline.TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            # save train and test numpy array and preprocessor object
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_obj(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)

            # save the preprocessor object
            save_obj("final_models/preprocessor.pkl",preprocessor_obj)

            # preparing the artifacts
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
        
    
        