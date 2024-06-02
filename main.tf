# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }
}

provider "azurerm" {
  features {}
}
# init data for keyvault
data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "ML-pipeline"
  location = var.region
}

# Generate a random integer to create a globally unique name
resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

# storage account for ML workspace
resource "azurerm_storage_account" "storage" {
  name                     = "mlpipeline${random_integer.ri.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# create app insights for creation of ML workspace
resource "azurerm_application_insights" "insights" {
  name                = "appinsights${random_integer.ri.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  application_type    = "web"
}



# init keyvault required for creation of ML workspace
resource "azurerm_key_vault" "vault" {
  name = "keyvault${random_integer.ri.result}"
  location = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id = data.azurerm_client_config.current.tenant_id
  sku_name = "premium"
}


resource "azurerm_machine_learning_workspace" "example" {
  name                    = "PDPworkspace${random_integer.ri.result}"
  location                = azurerm_resource_group.rg.location
  resource_group_name     = azurerm_resource_group.rg.name
  application_insights_id = azurerm_application_insights.insights.id
  key_vault_id            = azurerm_key_vault.vault.id
  storage_account_id      = azurerm_storage_account.storage.id

  identity {
    type = "SystemAssigned"
  }

}

# resource "null_resource" "custom_objects" {

#   provisioner "local-exec" {
#     command = <<-EOT
#       python compute_creation_config.py --rg-id ${rg.name}"
#     EOT
#     working_dir = "${path.module}/scripts" # works with ${path.root} as well
#   }
# }



