# Azure Bastion for RDP and SSH using Pulumi

This is a free to use (no guarantees given) [Pulumi](https://pulumi.com) module that can be used to deploy the Azure Bastion service into an existing subscription.

For more information about this service, read the [official Microsoft documentation on Azure Bastion](https://azure.microsoft.com/en-us/services/azure-bastion/).

## Requirements

* python 3.7
* authenticated session to Azure subscription
* pulumi cli

Please refer to the Microsoft documentation for any other prerequisites that might change over time.

## Deploy this example

Clone this repo and then run the following:

```
cd pulumi-azure-bastion
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
pulumi stack init pulumi-azure-bastion
pulumi config set azure:environment public
pulumi preview
```

If `pulumi preview` looks okay, then you can follow this up with `pulumi update` to deploy the stack.

## Destroy the infrastructure

When done testing this example please consider tearing the infrastructure down to save cost.

```
pulumi destroy
```