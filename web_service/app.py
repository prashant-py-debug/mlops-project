import os
import requests
from fastapi import FastAPI 
from schema import feature
from get_model import model
import warnings
from pymongo import MongoClient
import json

warnings.filterwarnings('ignore')

app = FastAPI()

RUN_ID = os.getenv('RUN_ID' , '14151288b1d54c558c607575a5031193')
EXP_ID = os.getenv('EXP_ID' , 1)

Model = model(logged_model=f"./artifacts/{EXP_ID}/{RUN_ID}/artifacts/banana-project-models")
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")

mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data")


@app.post("/prediction")
def predict(Input : feature):

    record = {'AT_1': Input.AT_1 , 'AT_2' : Input.AT_2}
    
    data = [[Input.AT_1 , Input.AT_2]]

    predict = Model.predict(data)

    
    save_to_db(record , predict[0])

    return {'predictions':predict[0]}


def save_to_db(record, prediction):
    rec = record.copy()
    rec['prediction'] = prediction
    collection.insert_one(rec)
