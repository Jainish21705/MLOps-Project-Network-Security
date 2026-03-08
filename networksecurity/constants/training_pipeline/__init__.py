import numpy as np
import pandas as pd
from datetime import datetime
import sys

TARGET_COLUMN = "result"
PIPELINE_NAME = "networksecurity"
ARTIFACT_NAME = "artifacts"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"


DATA_INGESTION_DATABASE_NAME = "NetworkSecurity"
DATA_INGESTION_COLLECTION_NAME = "dataset"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2
