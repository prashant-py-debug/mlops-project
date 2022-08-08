import mlflow

# mlflow.set_tracking_uri("http://localhost:5000")


def model(logged_model):
    """Load model as a PyFuncModel"""
    loaded_model = mlflow.pyfunc.load_model(logged_model)

    return loaded_model
