# import required libraries
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    ManagedOnlineEndpoint,
    ManagedOnlineDeployment,
    Model,
    Environment,
    CodeConfiguration,
)
from azure.identity import DefaultAzureCredential
import random

subscription_id = '167d566b-196d-4e96-aee0-0d2a1f78842e'
resource_group = 'ML-pipeline'
workspace = 'PDPworkspace87928'

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)


endpoint_name = "ML-endpt-" + str(random.randint(0, 10000))


def create_endpoint_deployment(model):
    endpoint = ManagedOnlineEndpoint(
    name=endpoint_name,
    description="deployment of ML-pipeline model",
    auth_mode="key",
    )
    ml_client.online_endpoints.begin_create_or_update(endpoint).result()

    # create model deployment on the endpoint
    blue_deployment = ManagedOnlineDeployment(
    name="blue-ML",
    endpoint_name=endpoint_name,
    model=model.id,
    instance_type="Standard_F4s_v2",
    instance_count=1,
    )

    ml_client.online_deployments.begin_create_or_update(blue_deployment)
