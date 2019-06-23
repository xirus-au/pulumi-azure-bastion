"""
Contains a Pulumi ComponentResource for creating a good-practice Azure Bastion resource.
"""
import json
from typing import Mapping, Sequence

import pulumi
from pulumi import Input
from pulumi_azure import network, core

class Bastion(pulumi.ComponentResource):
    """
    Creates a good-practice Azure Bastion service in an existing vnet
    """

    def __init__(self,
                 name: str,
                 location: None, resource_group_name: None, vnet_name: None, address_prefix: None,
                 opts: pulumi.ResourceOptions = None):
        super().__init__('Bastion', name, None, opts)

        # Make base info available to other methods
        self.name = name
        self.location = location
        self.resource_group_name = resource_group_name
        self.vnet_name = vnet_name
        self.address_prefix = address_prefix

        # Create Bastion Subnet

        self.subnet = network.Subnet("bastion-subnet",
                                     name="AzureBastionSubnet",
                                     resource_group_name=resource_group_name,
                                     virtual_network_name=vnet_name,
                                     address_prefix=address_prefix
                                     )

        # Create Public IP
        self.pip = network.PublicIp("bastion-pip",
                                    location=location,
                                    resource_group_name=resource_group_name,
                                    name=f"{name}-bastionpip",
                                    allocation_method="Static",
                                    sku="Standard"
                                    )

        # Deploy Bastion ARM template
        self.bastion = core.TemplateDeployment("bastion",
                                               deployment_mode="Incremental",
                                               resource_group_name=resource_group_name,
                                               template_body=json.dumps(
                                                   {
                                                       "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
                                                       "contentVersion": "1.0.0.0",
                                                       "parameters": {
                                                           "bastionHostName": {
                                                               "type": "string",
                                                               "metadata": {
                                                                   "description": "Bastion Name"
                                                               }
                                                           },
                                                           "location": {
                                                               "type": "string",
                                                               "metadata": {
                                                                   "description": "Location for all resources."
                                                               }
                                                           },
                                                           "bastionServicesVnetName": {
                                                               "type": "string",
                                                               "metadata": {
                                                                   "description": "Virtual Network Name"
                                                               }
                                                           },
                                                           "bastionServicesSubnetName": {
                                                               "type": "string",
                                                               "metadata": {
                                                                   "description": "Subnet Name"
                                                               }
                                                           },
                                                           "publicIpAddressName": {
                                                               "type": "string"
                                                           },
                                                           "COSTCENTRE": {
                                                               "type": "string",
                                                               "defaultValue": "1234"
                                                           },
                                                           "APPLICATION": {
                                                               "type": "string",
                                                               "defaultValue": "platform"
                                                           },
                                                           "ENVIRONMENT": {
                                                               "type": "string",
                                                               "defaultValue": "dev"
                                                           },
                                                       },
                                                       "variables": {
                                                           "subnetRefId": "[resourceId('Microsoft.Network/virtualNetworks/subnets', parameters('bastionServicesVnetName'), parameters('bastionServicesSubnetName'))]"
                                                       },
                                                       "resources": [
                                                           {
                                                               "apiVersion": "2018-10-01",
                                                               "type": "Microsoft.Network/bastionHosts",
                                                               "name": "[parameters('bastionHostName')]",
                                                               "location": "[parameters('location')]",
                                                               "properties": {
                                                                   "ipConfigurations": [
                                                                       {
                                                                           "name": "IpConf",
                                                                           "properties": {
                                                                               "subnet": {
                                                                                   "id": "[variables('subnetRefId')]"
                                                                               },
                                                                               "publicIPAddress": {
                                                                                   "id": "[resourceId('Microsoft.Network/publicIpAddresses', parameters('publicIpAddressName'))]"
                                                                               }
                                                                           }
                                                                       }
                                                                   ]
                                                               },
                                                               "tags": {}
                                                           }
                                                       ],
                                                       "outputs": {}
                                                   }),
                                               parameters={
                                                   "bastionHostName": location.apply(lambda location: location + "-bastion"),
                                                   "publicIpAddressName": self.pip.name,
                                                   "location": location,
                                                   "bastionServicesVnetName": vnet_name,
                                                   "bastionServicesSubnetName": self.subnet.name
                                               }
                                               )

        super().register_outputs({})
