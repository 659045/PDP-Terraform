# PDP-Terraform
PDP Week6

PREREQUISITES

Have terraform installed

Install the required packages

TO RUN EXECUTE THE FOLLOWING:

```terraform init```

```terraform apply```



To deploy a compute cluster:

install the required packages

``` compute_creation_config.py --sub-id=<subscription_id> --rg=<resource_group_name> --workspace-name=<workspace_name> --compute-name=<compute_cluster_name> ```

In order to run the training and deployment of the model:
install the required packages

``` run_pl.py --sub-id=<subscription_id> --rg=<resource_group_name> --workspace-name=<workspace_name> --compute-name=<compute_cluster_name>```

