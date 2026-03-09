import os
import sys
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import pickle
import pandas as pd
import numpy as np
# import dill

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def write_yaml_file(file_path: str, data: object, replace: bool = False):
    try:
        dir_path = os.path.dirname(file_path)

        # Create directory if not exists
        os.makedirs(dir_path, exist_ok=True)

        # Remove file if replace=True
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        # Write yaml
        with open(file_path, "w", encoding="utf-8") as yaml_file:
            yaml.dump(data, yaml_file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

def read_data(file_path:str)->pd.DataFrame:
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_obj(file_path:str,obj:object):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)