from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

from azure.ai.ml import MLClient, Input, command
from azure.ai.ml.dsl import pipeline
from azure.ai.ml import load_component
from azure.ai.ml.entities import Model
from azure.ai.ml.constants import AssetTypes
import time
import dlp_model
import argparse
import sys
credential = DefaultAzureCredential()


parser = argparse.ArgumentParser()
parser.add_argument("--sub-id", type=str)
parser.add_argument("--rg", type=str)
parser.add_argument("--workspace-name", type=str)
parser.add_argument("--compute-name", type=str, default="cpu-cluster")


args = parser.parse_args()

subscription_id = args.sub_id
resource_group = args.rg
workspace = args.workspace_name


if not subscription_id or not resource_group or not workspace:
    print("use: run_pl.py --sub-id=<subscription_id> --rg=<resource_group_name> --workspace-name=<workspace_name> --compute-name=<compute_cluster_name>")
    sys.exit()


#connect to the workspace
ml_client = MLClient(credential, subscription_id, resource_group, workspace)


# define the command
command_job = command(
    code="",
    command="python model.py --data ${{inputs.soccer_csv}} --learning-rate ${{inputs.learning_rate}} --boosting ${{inputs.boosting}}",
    environment="AzureML-lightgbm-3.2-ubuntu18.04-py37-cpu@latest",
    inputs={
        "soccer_csv": Input(
            type="uri_file",
            path="Soccer2019s.csv",
        ),
        "learning_rate": 0.9,
        "boosting": "gbdt",
    },
    compute="cpu-cluster",
)

returned_job = ml_client.jobs.create_or_update(command_job)
# get a URL for the status of the job

job_id = returned_job.name
print(f"Launched job {job_id}, awaiting completion...")

while True:
    job_status = ml_client.jobs.get(job_id).status
    if job_status in ['Completed', 'Failed', 'Canceled']:
        break
    print(f"Job status: {job_status}")
    time.sleep(30) # reiterate job_status every 10 secs

if job_status != 'Completed':
    raise Exception(f"Job did not complete succesfully: {job_status}")


job = ml_client.jobs.get(job_id)

# Register model
model = Model(
    path="azureml://jobs/{}/outputs/artifacts/paths/model/".format(job_id),
    name="Toph-aut",
    description="Model automated through Azure-SDK",
    type=AssetTypes.MLFLOW_MODEL
)

reg_model = ml_client.models.create_or_update(model)
print(f"Model registered: {reg_model.name} with version: {reg_model.version}")


dlp_model.create_endpoint_deployment(reg_model)



