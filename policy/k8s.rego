package main

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  endswith(c.image, ":latest")
  msg := sprintf("DENY: image uses :latest (%s). Pin to a sha tag or digest.", [c.image])
}

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  not c.readinessProbe
  msg := sprintf("DENY: container %s missing readinessProbe", [c.name])
}

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  not c.livenessProbe
  msg := sprintf("DENY: container %s missing livenessProbe", [c.name])
}

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  not c.resources.limits.cpu
  msg := sprintf("DENY: container %s missing cpu limit", [c.name])
}

deny[msg] {
  input.kind == "Deployment"
  c := input.spec.template.spec.containers[_]
  not c.resources.limits.memory
  msg := sprintf("DENY: container %s missing memory limit", [c.name])
}
