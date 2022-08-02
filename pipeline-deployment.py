from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule
from prefect.flow_runners import SubprocessFlowRunner
from datetime import timedelta



DeploymentSpec(
    name="Banana-model-pipeline",
    flow_location="training_pipeline.py",
    flow_runner = SubprocessFlowRunner(),
    schedule=IntervalSchedule(interval = timedelta(minutes = 10)),
    tags = ['ml']
)



