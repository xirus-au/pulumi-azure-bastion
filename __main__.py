import pulumi
from pulumi_azure import core, network
from bastion import bastion

# Create an Azure Resource Group
resource_group = core.ResourceGroup("resource_group", 
    location='australiaeast')

vnet = network.VirtualNetwork("vnet",
    location=resource_group.location,
    resource_group_name=resource_group.name,
    address_spaces=["10.0.0.0/8"]
)

bastion = bastion.Bastion("bastion",
    location=resource_group.location,
    resource_group_name=resource_group.name,
    address_prefix="10.1.0.0/24",
    vnet_name=vnet.name
)