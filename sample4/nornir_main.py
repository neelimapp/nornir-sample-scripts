#!/usr/bin/env python3
  
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli, napalm_configure
from nornir.core.task import Task

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

rt1 = nr.filter(name="rt1")

def multiple_tasks(task: Task):
    task.run(
        task=napalm_cli, commands=["show interfaces brief"]
    )
    
    task.run(
        task=napalm_configure, dry_run=False, configuration="interface loopback 1000"
    )

    task.run(
        task=napalm_get, getters=["interfaces"]
    )

results = rt1.run(
    task=multiple_tasks
)

print_result(results)

