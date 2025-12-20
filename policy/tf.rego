package main

deny[msg] {
  # For terraform show -json plan output:
  some rc
  rc := input.resource_changes[_]
  rc.type == "aws_security_group_rule"
  after := rc.change.after
  cidrs := after.cidr_blocks
  cidrs[_] == "0.0.0.0/0"
  msg := sprintf("DENY: %s opens 0.0.0.0/0", [rc.address])
}

deny[msg] {
  # Azure example: NSG rule allowing 0.0.0.0/0
  some rc
  rc := input.resource_changes[_]
  rc.type == "azurerm_network_security_rule"
  after := rc.change.after
  after.source_address_prefix == "*"
  after.destination_address_prefix == "*"
  msg := sprintf("DENY: %s allows open traffic (* -> *)", [rc.address])
}
