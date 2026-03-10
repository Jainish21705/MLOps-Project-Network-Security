import numpy as np
import pandas as pd
from datetime import datetime
import sys
import os

TARGET_COLUMN = "Result"
PIPELINE_NAME = "networksecurity"
ARTIFACT_NAME = "artifacts"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")
SAVED_MODEL_PATH = os.path.join("saved_models")


DATA_INGESTION_DATABASE_NAME = "NetworkSecurity"
DATA_INGESTION_COLLECTION_NAME = "dataset"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2


DATA_VALIDATION_DIR = "data_validation"
DATA_VALIDATION_VALID_DIR = "validated"
DATA_VALIDATION_INVALID_DIR = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME = "report.yaml"

DATA_TRANSFORMATION_DIR_NAME = "data_transformation"
DATA_TRANSFORMATION_DATA_DIR = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR = "transformed_object"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME = "transformed_object.pkl"

# knn imputer params
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

MODEL_TRAINER_DIR = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR="trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_PATH="model.pkl"
MODEL_TRAINER_EXCEPTED_SCORE:float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD:float = 0.05

TRAINING_BUCKET_NAME = "testnetworksecurity2107"

