import os
import warnings
import pandas as pd
import numpy as np
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split , RandomizedSearchCV
from sklearn.metrics import accuracy_score
from prefect import flow , task
from prefect.task_runners import SequentialTaskRunner


warnings.filterwarnings("ignore")

DATA_PATH = os.getenv("DATA path" , "banana/banana.csv")

@task
def set_mlflowTracking():
    mlflow.set_tracking_uri("http://localhost:5000")


@task
def load_data(path):
    '''
    loads data from csv file
    '''

    data = pd.read_csv(path , names=['At1' , 'At2' , 'Class'])
    X = data.drop(columns = 'Class')
    y = data.Class
    return X,y


def prepare(X,y):
    '''
    splits data into train and test set
    '''
    
    X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.2 , random_state=1234 )

    return X_train , X_test , y_train , y_test

@task
def hyperparameter_tunning(X,y):
    '''
    Does hyperparameter tunning
    '''

    rf = RandomForestClassifier(random_state=42)

    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]


    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}

    rf_random = RandomizedSearchCV(estimator = rf, 
    param_distributions = random_grid, n_iter = 10, 
    cv = 3, verbose=2, random_state=42, n_jobs = -1 )

    

    rf_random.fit(X,y)
    
    all_results = pd.DataFrame(rf_random.cv_results_)
    
    
    for i in range(len(all_results)):
        with mlflow.start_run():
            mlflow.set_experiment("Banana Experiment")
            mlflow.set_tag('model','random_forest')
            parameters = all_results['params'][i]
            mlflow.log_params(parameters)
            
            mlflow.log_metric('accuracy',all_results['mean_test_score'][i])
    
            
    return rf_random.best_params_

@task
def train_best_model(best_param,X,y):

    with mlflow.start_run():
        mlflow.set_experiment("Banana Experiment")
        mlflow.set_tag('model','best_random_forest')
        mlflow.log_params(best_param)
        rf = RandomForestClassifier(random_state=42,**best_param )
        X_train , X_test , y_train , y_test = prepare(X,y)

        rf.fit(X_train,y_train)
        y_pred = rf.predict(X_test)
        score = accuracy_score(y_test,y_pred)

        mlflow.log_metric("accuracy",score)

        mlflow.sklearn.log_model(sk_model=rf,
        artifact_path="banana-project-models",
        registered_model_name="sk-learn-random-forest-classifier-model"
        )

@flow(task_runner=SequentialTaskRunner())
def pipeline():

    set_mlflowTracking()
    X,y = load_data(DATA_PATH).result()
    best_params = hyperparameter_tunning(X,y).result()
    train_best_model(best_params,X,y)


if __name__ == "__main__":
    pipeline()
    
    

    




