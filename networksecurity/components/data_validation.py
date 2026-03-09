from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.logging.logger import logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file,read_data,write_yaml_file
import sys
import os
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            actual_number_of_columns = len(self._schema_config["columns"])
            dataframe_number_of_columns = len(dataframe.columns)
            logger.info("Actual number of columns: {0} and dataframe number of columns {1}".format(actual_number_of_columns,dataframe_number_of_columns))
            if actual_number_of_columns == dataframe_number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def validate_number_of_numeric_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            actual_number_of_numeric_columns = len(self._schema_config["numerical_columns"])
            dataframe_number_of_numeric_columns = len(dataframe.columns)
            logger.info("Actual number of numeric columns: {0} and dataframe number of numeric columns {1}".format(actual_number_of_numeric_columns,dataframe_number_of_numeric_columns))
            if actual_number_of_numeric_columns == dataframe_number_of_numeric_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def checking_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    is_found = True
                    status = False
                report.update({
                    column:{
                        "p_value":float(is_same_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            write_yaml_file(drift_report_file_path, report)

            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
   
    def initate_data_validation(self):
        try:
            # load the data from the given data ingestion artifact
            trained_file_path = self.data_ingestion_artifact.trained_file_path
            tested_file_path = self.data_ingestion_artifact.tested_file_path

            train_df = read_data(trained_file_path)
            test_df = read_data(tested_file_path)

            # validate the number of columns
            validate_number_of_columns_trained_df_status = self.validate_number_of_columns(train_df)
            if not validate_number_of_columns_trained_df_status:
                error_message = f"Train dataframe has different number of columns than expected {len(self._schema_config['columns'])} columns"

            validate_number_of_columns_test_df_status = self.validate_number_of_columns(test_df)
            if not validate_number_of_columns_test_df_status:
                error_message = f"Test dataframe has different number of columns than expected {len(self._schema_config['columns'])} columns"

            
            # validate the numeric columns exist or not
            validate_number_of_numeric_columns_trained_df_status = self.validate_number_of_numeric_columns(train_df)
            if not validate_number_of_numeric_columns_trained_df_status:
                error_message = f"Train dataframe has different number of numeric columns than expected {len(self._schema_config['numerical_columns'])} columns"

            validate_number_of_numeric_columns_test_df_status = self.validate_number_of_numeric_columns(test_df)
            if not validate_number_of_numeric_columns_test_df_status:
                error_message = f"Test dataframe has different number of numeric columns than expected {len(self._schema_config['numerical_columns'])} columns"

            # checking the data drift
            data_drift_status = self.checking_data_drift(train_df,test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=data_drift_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            ) 

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)