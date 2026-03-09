import os
import sys
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
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

def load_numpy_array_data(file_path:str):
     try:
        if not os.path.exists(file_path):
            raise Exception(f"The given {file_path} does not exist")
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
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

def load_obj(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The given {file_path} does not exist")
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def evaulate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}

        for model_name, model in models.items():

            para = params[model_name]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)

            report[model_name] = test_acc

        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)