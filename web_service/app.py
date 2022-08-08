import os
import warnings
from fastapi import FastAPI 
from schema import feature
from get_model import model
from pymongo import MongoClient


warnings.filterwarnings('ignore')

app = FastAPI()

RUN_ID = os.getenv('RUN_ID' , '14151288b1d54c558c607575a5031193')
EXP_ID = os.getenv('EXP_ID' , 1)

Model = model(
logged_model=f"./artifacts/{EXP_ID}/{RUN_ID}/artifacts/banana-project-models")
MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")

mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database("prediction_service")
collection = db.get_collection("data")


@app.post("/prediction")
def predict(Input : feature):
    '''api to do predictions'''
    record = {'AT_1': Input.AT_1 , 'AT_2' : Input.AT_2}
    
    data = [[Input.AT_1 , Input.AT_2]]

    pred = Model.predict(data)

    
    save_to_db(record , pred[0])

    return {'predictions':pred[0]}


def save_to_db(record, prediction):
    
    'save data to db'

    rec = record.copy()
    rec['prediction'] = prediction
    collection.insert_one(rec)
