# Jargon Buster Backend - on Azure Web App for Containers

This backend app runs on Python / Flask. It's the backend to the
Jargon Buster Frontend Static Web App found here: ...

Architecture Diagram:


Here's how to get it running on Azure.


# Create a Service Principal
```bash
AZURE_SUB_ID=<Your Azure Subscription ID>
RESOURCE_GROUP=<Your ResourceGroup name, e.g. 'HealthHack'>

az ad sp create-for-rbac -n "JargonBusterBackend" --role contributor \
   --scopes /subscriptions/$AZURE_SUB_ID/resourceGroups/$RESOURCE_GROUP > ServicePrincipal.json

cat ServicePrincipal.json
``` 

# Create
```bash
#!/bin/bash

# Based on: https://docs.microsoft.com/en-us/azure/app-service/scripts/cli-linux-docker-aspnetcore#sample-script

# Variables
appName=$1
appPlanName="${appName}plan"
resGroupName=$2
location="WestUS2"

# Create a Resource Group
az group create –name $resGroupName –location $location

# Create an App Service Plan
az appservice plan create –name $appPlanName –resource-group $resGroupName –location $location –is-linux –sku B1

# Create a Web App
az webapp create –name $appName –plan $appPlanName –resource-group $resGroupName –runtime "python|3.8"

# Copy the result of the following command into a browser to see the web app.
echo http://$appName.azurewebsites.net
```

 
# Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
