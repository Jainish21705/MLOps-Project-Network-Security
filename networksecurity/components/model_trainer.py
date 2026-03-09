from  networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
import os,sys
import numpy as np
import pandas as pd
import mlflow

from networksecurity.utils.main_utils.utils import save_obj,load_obj,load_numpy_array_data,evaulate_models
from networksecurity.utils.ml_utils.metric.classfication_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier,
    GradientBoostingClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import r2_score

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model_name:str,best_model,classification_train_metric:dict):
        try:
            f1_score = classification_train_metric.f1_score
            precision = classification_train_metric.precision
            recall = classification_train_metric.recall

            mlflow.log_params({"best_model_name":best_model_name})
            mlflow.log_metrics({"f1_score":f1_score,"precision":precision,"recall":recall})
            mlflow.sklearn.log_model(best_model,"Model")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_model(self,X_train,y_train,X_test,y_test):
        models = {
            "Decision_Tree":DecisionTreeClassifier(),
            "Random_Forest":RandomForestClassifier(verbose=1),
            "Gradient_Boosting":GradientBoostingClassifier(verbose=1),
            "Logistic_Regression":LogisticRegression(verbose=1),
            "AdaBoost_classfier":AdaBoostClassifier(),
        }

        params = {
            "Decision_Tree":{
                "criterion":['gini','entropy']
            },
            "Random_Forest":{
                "n_estimators":[8,16,128,256]
            },
            "Gradient_Boosting":{
                "learning_rate":[0.1,0.01],
                "n_estimators":[8,16,32,64]
            },
            "Logistic_Regression":{},
            "AdaBoost_classfier":{
                "learning_rate":[0.1,0.01],
                "n_estimators":[8,16,32,64,128,256]
            }
        }

        model_report:dict = evaulate_models(X_train,y_train,X_test,y_test,models,params)

        # to get the best model score from dict
        best_model_score = max(sorted(model_report.values()))

        # to get the best model name from dict

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]

        best_model = models[best_model_name]

        # track the mlflow

        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(
            y_true=y_train,y_pred=y_train_pred
        )

        self.track_mlflow(best_model_name,best_model,classification_train_metric)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(
            y_true=y_test,y_pred=y_test_pred
        ) 

        self.track_mlflow(best_model_name,best_model,classification_test_metric)

        preprocessor = load_obj(file_path=self.data_transformation_artifact.transformed_object_file_path)
        dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(dir_path,exist_ok=True)

        Network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
        save_obj(file_path=self.model_trainer_config.trained_model_file_path,obj=Network_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )

        return model_trainer_artifact

    def initate_model_trainer(self)-> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # load the data from numpy arrays
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            # split the datasset
            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1],
            )

            model_trainer_artifact = self.train_model(
                X_train=x_train,y_train=y_train,X_test=x_test,y_test=y_test
            )

            return model_trainer_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        