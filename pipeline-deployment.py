from datetime import timedelta
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect.flow_runners import SubprocessFlowRunner


DeploymentSpec(
    name="Banana_model_pipeline",
    flow_location="training_pipeline.py",
    flow_runner=SubprocessFlowRunner(),
    schedule=IntervalSchedule(interval=timedelta(minutes=10)),
    tags=["ml"],
)
