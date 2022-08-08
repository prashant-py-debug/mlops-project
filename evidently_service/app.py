import os
import warnings
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from evidently.dashboard import Dashboard
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.dashboard.tabs import DataDriftTab, NumTargetDriftTab
from pymongo import MongoClient



warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')




MONGODB_ADDRESS = os.getenv("MONGODB_ADDRESS", "mongodb://127.0.0.1:27017")
mongo_client = MongoClient(MONGODB_ADDRESS)
db = mongo_client.get_database("prediction_service")
window_size = 500

app = FastAPI()

def get_data_from_db():
    """fetch data from db"""
    collection = db.get_collection("data")
    data = list(collection.find())
    
    if len(data) < window_size:
        return data

    return data
    

def preprocess(List):
    """preprocess fetched data to compare with ref data"""
 
    prod_dict = {'AT_1': [] , 'AT_2': [] , 'Class':[]}
    for obj in List:
        prod_dict['AT_1'].append(obj['AT_1'])
        prod_dict['AT_2'].append(obj['AT_2'])
        prod_dict['Class'].append(obj['prediction'])
    prod_df = pd.DataFrame.from_dict(prod_dict)
    return prod_df




def create_dashboard():
    """create dashboard"""

    prod_data_sample = get_data_from_db()
    if len(prod_data_sample) < window_size :
        return "Not enough data to create report, please refresh after some time!"
    ref_data_sample = pd.read_csv("banana.csv" , names=['AT_1' , 'AT_2' , 'Class'])
    prod_data_sample = preprocess(prod_data_sample)
    numerical_features = ['AT_1' , 'AT_2']
    target = 'Class'
    column_mapping = ColumnMapping()
    column_mapping.target = target
    column_mapping.numerical_features = numerical_features

    data_drift_dashboard = Dashboard(
        tabs= [DataDriftTab(verbose_level=1),
        NumTargetDriftTab(verbose_level=1)])
        
    data_drift_dashboard.calculate(ref_data_sample, 
                        prod_data_sample, 
                        column_mapping=column_mapping)

    try:
        os.mkdir("dashboards")
    except:
        pass

    data_drift_dashboard.save('./dashboards/data_drift.html')




@app.get("/get_dashboard")
async def data_drift():
    """api to get dashboard"""
    create_dashboard()
    with open("./dashboards/data_drift.html" , "r",encoding='utf-8') as file:
        dashboard = file.read()
        

    return HTMLResponse(content=dashboard, status_code=200)



