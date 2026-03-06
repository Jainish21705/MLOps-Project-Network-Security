import os
import sys
import json
import certifi
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from dotenv import load_dotenv
import pandas as pd
import numpy as np

load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

ca = certifi.where()

class NetworkExtractData():
    def __int__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json_converter(self,filepath:str):
        try:
            df = pd.read_csv(filepath)
            df.reset_index(drop=True,inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def inject_data_into_db(self,records,database,connection):
        self.database = database
        self.connection = connection
        self.records = records
        self.mongo_db_client = pymongo.MongoClient(MONGO_DB_URI)
        self.database = self.mongo_db_client[self.database]
        self.connection = self.database[self.connection]

        self.connection.insert_many(records)
        return len(self.records)

if __name__=='__main__':
    filepath = 'Network_Data\phisingData.csv'
    database = 'NetworkSecurity'
    collection = 'dataset'
    netwrokobj = NetworkExtractData()
    records = netwrokobj.csv_to_json_converter(filepath)
    length = netwrokobj.inject_data_into_db(records,database,collection)
    print(length)



