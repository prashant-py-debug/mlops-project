# to run the pipeline orchestration

## to start the mlflow and prefect server
1. mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./artifacts
2. prefect orion start

## create the storage for prefect
1. prefect storage create 
2. select local storage
3. give path "./.prefect"
4. prefect storage ls
5. copy the id of storage
6. prefect storage set-default <id>

## deploy the training flow
1. prefect deployment create pipeline-deployment.py
2. Create a worker with subprocess using the prefect ui
3. prefect agent start <workerid>