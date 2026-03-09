import os
import sys

import certifi
ca = certifi.where()

from dotenv import  load_dotenv
load_dotenv()
MONGO_DB_URI = os.getenv("MONGO_DB_URI")

import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse ,HTMLResponse
import pandas as pd
from networksecurity.utils.main_utils.utils import load_obj

client = pymongo.MongoClient(MONGO_DB_URI, tlsCAFile=ca)
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/",tags=['Authentication'])
def home():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocesor = load_obj("final_models/preprocessor.pkl")
        final_model = load_obj("final_models/model.pkl")

        network_model = NetworkModel(preprocessor=preprocesor, model=final_model)

        y_pred = network_model.predict(df)

        df["predicted_column"] = y_pred

        table_html = df.to_html(classes="table table-striped")

        return table_html
        
    except Exception as e:
            raise NetworkSecurityException(e,sys)

if __name__=='__main__':
    app_run("app:app",host="0.0.0.0",port=8000,reload=True)


