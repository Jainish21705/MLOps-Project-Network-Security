from networksecurity.constants.training_pipeline import SAVED_MODEL_PATH,MODEL_TRAINER_TRAINED_MODEL_FILE_PATH
from networksecurity.exception.exception import NetworkSecurityException
import os,sys

class NetworkModel:
    def __init__(self,preprocessor,model):
        self.preprocessor = preprocessor
        self.model = model
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        