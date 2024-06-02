#import required libraries
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml.entities import AmlCompute
import argparse
import sys

credential=DefaultAzureCredential()

parser = argparse.ArgumentParser()
parser.add_argument("--sub-id", type=str)
parser.add_argument("--rg", type=str)
parser.add_argument("--workspace-name", type=str)
parser.add_argument("--compute-name", type=str, default="cpu-cluster")


args = parser.parse_args()

subscription_id = args.sub_id
resource_group = args.rg
workspace = args.workspace_name
compute_name = args.compute_name

#connect to the workspace
ml_client = MLClient(credential, subscription_id, resource_group, workspace)



try:
    ml_client.compute.get(cpu_compute_target)
except Exception:
    print("Creating a new cpu compute target...")
    compute = AmlCompute(
        name=compute_name, size="STANDARD_D2_V2", min_instances=0, max_instances=1
    )
    ml_client.compute.begin_create_or_update(compute).result()