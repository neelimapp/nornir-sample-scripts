
# Nornir Overview

Are you looking for a flexible, scalable, efficient network automation framework, where all tasks are written in Python programming language? If yes, then you are at the right place! And it is Nornir !!!

## Ok! Now, what is Nornir?
Nornir is a multi-threaded network automation framework that abstracts inventory and task execution. It helps to automate your network tasks efficiently. You can execute the tasks like configuring the devices, validating the operational data, and enabling the services on the provided hosts which are part of the inventory. As it is multithreaded, it allows you to manage the configuration of multiple network devices concurrently. It is an open-source project, completely written in python and easy to use. You should write a simple python code to make use of Nornir features.

## Well, why Nornir?
- Firstly, it is an open-source project, hence it is free to use and you can develop features on top of the Nornir framework based on your requirement.
- It has an active community and well-maintained documentation.
- As Nornir is completely written in python, it is easy to
	- install
	- write code
	- integrate with any other python frameworks (Flask, Django, Pytest)
	- troubleshoot and debug the issues using python debug tools
- It reuses existing python libraries like Netmiko and Napalm to connect and manage the devices.
- The use of multithreading greatly optimizes the execution time of the tasks.
- You can effectively manage the hosts and groups separately as part of the inventory.

## So, how does it work?

### Setup virtual environment(Optional)

If you would like to isolate the dependencies of Nornir from the system, you can create a python virtual environment.

Install virtualenv package using pip. pip is a package installer for Python. Here I am using Python 3.7.3 version.
```
pip install virtualenv
```
Using virtualenv package, create a python virtual environment.
Refer [creation of python virtual environments](https://docs.python.org/3/library/venv.html).
```
virtualenv nornir_venv
```
Now activate the virtual environment.
```
source ~/nornir_venv/bin/activate
```
### Install Nornir and its plugins

In the “nornir_venv” virtual environment, install **nornir**. At the moment of producing this tutorial latest version of nornir is 3.0.0.
```
pip install nornir
```
Install Nornir plugin nornir-napalm. It provides napalm `connections` through which you connect to the device and execute `tasks` like `napalm_cli`, `napalm_configure`, `napalm_get`, `napalm_ping`, and `napalm_validate`. 

- If you assign `task=napalm_cli` in nornir, then you can execute the napalm CLI method with the provided CLI commands. For example `commands=["show interfaces"]`.
- If you assign `task=napalm_configure`, you can configure the devices with the provided configuration or filename. For example `configuration="hostname nornir"`.
- If you assign `task=napalm_get`, you can execute napalm getters with the provided getter methods. For example `getters=["interfaces"]`.
- If you assign `task=napalm_ping`, you can execute the napalm ping method with the provided destination address. For example `dest="172.11.4.5"`.
- If you assign `task=napalm_validate`, you can validate device configuration with the provided validation source or filename. For example `validation_source=[{"get_interfaces": {"GigabitEthernet1": {"description": ""}}}]`.
```
pip install nornir-napalm
```
Install Nornir plugin **nornir-utils**. It provides plugins like `inventory`, `functions`, `processors`, and `tasks`.

- The inventory offers a `YAMLInventory` plugin to load data from YAML files.
- Functions offer `print_result`, `print_title` helper functions to format and print the result/title as the output.
- Processors offer `PrintResult` addon to print information of task execution.
- Tasks offer addons like `echo_data` to echo the data passed to it, `load_json` to load JSON file, `load_yaml` to load YAML file and `write_file` to write content to the file.
```
pip install nornir-utils
```
Once you have all the required packages installed, go ahead and write the code to retrieve, configure or validate device data.

### Write a few lines of code to automate your network

![image](https://user-images.githubusercontent.com/10559258/124207329-207fd780-da9a-11eb-8569-5ba00b402d8a.png)

#### Example 1

Create a directory called inventory and in that create the inventory files `hosts.yaml`, `groups.yaml`, and `defaults.yaml`.

**hosts.yaml**
```
# hosts.yaml
---
rt1:
   hostname: 171.190.10.64
   groups:
        - iosxr
rt2:
   hostname: 10.30.11.170
   groups:
        - ios
```
**groups.yaml**
```
# groups.yaml
---
iosxr:
    platform: 'iosxr'
ios:
    platform: 'ios'
```

**defaults.yaml**
```
# defaults.yaml
username: admin
password: admin
```
FYI, execute below python code to understand the schema of the objects (hosts, groups, defaults).
```
from nornir.core.inventory import Host, Group, Defaults
import json

print(json.dumps(Host.schema(), indent=4))
print(json.dumps(Group.schema(), indent=4))
print(json.dumps(Defaults.schema(), indent=4))                                           
```

Now come out of the inventory directory and create a config file that provides information about the inventory and runner to the main file.

**config.yaml**
```
# config.yaml
---
inventory:
       plugin: SimpleInventory
       options:
            host_file: 'inventory/hosts.yaml'
            group_file: 'inventory/groups.yaml'
            defaults_file: 'inventory/defaults.yaml'
runner:
       plugin: threaded
       options:
            num_workers: 2
```
Config file provides inventory and task parallelization information to the main file. Nornir will use a different thread for each host to concurrently execute the tasks of the hosts. You can provide the number of threads to be used by your code in the `num_workers` option of the runner plugin. If `num_workers == 1`, tasks of the hosts are executed one after the other in a simple loop. This case helps to troubleshoot or debug the issues. Generally, you can provide a number greater than 1 to `num_workers` else it defaults to 20. In my case, I am assigning value 2 to `num_workers`, as I am dealing with two hosts.

**nornir_main.py**
```
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

results = nr.run(
    task=napalm_get, getters=["facts"]
)

print_result(results)
```
This is the main file where you initialize Nornir with the `InitNornir` function and provide the configuration file. In the next step, call a run method and provide the tasks to be executed, here we provided `napalm_get`, imported from the `nornir_napalm` plugin. It executes the provided napalm getters over all the hosts provided in the inventory and returns the results.

Execute **nornir_main.py** file and retrieve the results.
```
python nornir_main.py
```
**Output**
```
napalm_get**********************************************************************
* rt1 ** changed : False *******************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'pavarotti',
	     'hostname': 'pavarotti',
             'interface_list': [ 'GigabitEthernet0/0/0/0',
                                 'GigabitEthernet0/0/0/1',
                                 'Loopback0',
                                 'MgmtEth0/RP0/CPU0/0',
				 'Null0'],
             'model': 'R-IOSXRV9000-CC',
             'os_version': '6.5.3',
             'serial_number': 'E3FDA081DAC',
             'uptime': 18033322,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* rt2 ** changed : False *******************************************************
vvvv napalm_get ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'facts': { 'fqdn': 'placido.placido.local',
             'hostname': 'placido',
             'interface_list': [ 'GigabitEthernet1',
				 'GigabitEthernet2',
				 'GigabitEthernet3'],
	     'model': 'CSR1000V',
	     'os_version': 'Virtual XE Software '
			   '(X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.9.3, '
	                   'RELEASE SOFTWARE (fc2)',
	     'serial_number': '9NSHRXZD4TZ',
             'uptime': 43016280,
             'vendor': 'Cisco'}}
^^^^ END napalm_get ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
The output shows the facts (napalm getter) retrieved from the hosts provided in the inventory. For every host the tasks are executed separately by a thread, hence the results are shown per host. It returns a dictionary for each host, with the key being the napalm getter name and value being the result of executing the getter method.

#### Example 2

 **Execute tasks without config file**
 
 In this case, you just need to create a host file and nornir main file.
 
 **hosts.yaml**
 
 ```
 # hosts.yaml
---
rt1:
    hostname: pavarotti
    platform: 'iosxr'
    username: admin
    password: admin

rt2:
    hostname: placido
    platform: 'ios'
    username: admin
    password: admin
```
If the inventory is not provided while initializing Nornir, It checks for hosts.yaml file with all the information of the hosts, hence all the details of the hosts are provided in a single hosts.yaml file.

**nornir_main.py**

```
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_cli

nr = InitNornir()

results = nr.run(
    task=napalm_cli, commands=["show interfaces summary"]
)

print_result(results)
```
This is the main file where you initialize Nornir with the `InitNornir` function and do not provide the configuration file. In the next step, call a run method and provide the tasks to be executed, here we provided `napalm_cli` imported from the `nornir_napalm` plugin. It executes the provided napalm CLI command over all the hosts provided in the hosts.yaml file and returns the results. As threading information is not provided in `InitNornir()`, here `num_workers` defaults to 20.

Execute **nornir_main.py** file and retrieve the results.
```
python nornir_main.py
```

**Output**

```
napalm_cli**********************************************************************
* rt1 ** changed : False *******************************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'show interfaces summary': 'Interface Type          Total    UP       '
                             'Down     Admin Down\n'
                             '--------------          -----    --       '
                             '----     ----------\n'
                             'ALL TYPES               5        5        '
                             '0        0       \n'
                             '--------------         \n'
                             'IFT_GETHERNET           2        2        '
                             '0        0       \n'
                             'IFT_LOOPBACK            1        1        '
                             '0        0       \n'
                             'IFT_ETHERNET            1        1        '
                             '0        0       \n'
                             'IFT_NULL                1        1        '
                             '0        0'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* rt2 ** changed : False *******************************************************
vvvv napalm_cli ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'show interfaces summary': '*: interface is up\n'
                             ' IHQ: pkts in input hold queue     IQD: pkts '
                             'dropped from input queue\n'
                             ' OHQ: pkts in output hold queue    OQD: pkts '
                             'dropped from output queue\n'
                             ' RXBS: rx rate (bits/sec)          RXPS: rx rate '
                             '(pkts/sec)\n'
                             ' TXBS: tx rate (bits/sec)          TXPS: tx rate '
                             '(pkts/sec)\n'
                             ' TRTL: throttle count\n'
                             '\n'
                             '  Interface                   IHQ       '
                             'IQD       OHQ       OQD      RXBS      RXPS      '
                             'TXBS      TXPS      TRTL\n'
                             '-----------------------------------------------------------------------------------------------------------------\n'
                             '* GigabitEthernet1              0         '
                             '0         0         0         0         '
                             '0         0         0         0\n'
                             '  GigabitEthernet2              0         '
                             '0         0         0         0         '
                             '0         0         0         0\n'
                             '  GigabitEthernet3              0         '
                             '0         0         0         0         '
                             '0         0         0         0'}
^^^^ END napalm_cli ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
The output shows the "interfaces summary" retrieved from the hosts provided in the hosts.yaml file. For every host the tasks are executed separately by a thread, hence the results are shown per host. It returns a dictionary for each host, with the key being the CLI command and value being the result of executing the CLI command.

#### Example 3

**Execute multiple napalm tasks**

**nornir_main.py**
```
#!/usr/bin/env python3
  
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get, napalm_cli, napalm_configure
from nornir.core.task import Task

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)

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

results = nr.run(
    task=multiple_tasks
)

print_result(results)
```
This is the main file where we initialize Nornir with the `InitNornir` function and provide the configuration file. In the next step, create a method(`multiple_tasks`) with Task object as its argument and provide the multiple tasks to be executed. Here we are calling a `run` method of `Task` object and providing the tasks (`napalm_cli`, `napalm_configure`, `napalm_get`) which retrieves results of `show interfaces brief`, configures `interface loopback 1000`, and retrieves interfaces. Then call a run method of nornir and provide the task to be executed, here we provided `multiple_tasks` which has different tasks in it. It executes the tasks over all the hosts provided in the inventory and returns the results.

Execute **nornir_main.py** file and retrieve the results.
```
./nornir_main.py
```
**Output**
```
multiple_tasks******************************************************************
* rt1 ** changed : True ********************************************************
vvvv multiple_tasks ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- napalm_cli ** changed : False --------------------------------------------- INFO
{ 'show interfaces brief': 'Intf       Intf        LineP              Encap  '
                           'MTU        BW\n'
                           '               Name       State       '
                           'State               Type (byte)    (Kbps)\n'
                           '--------------------------------------------------------------------------------\n'
                           '                Lo0          up          '
                           'up           Loopback  1500          0\n'
                           '     Mg0/RP0/CPU0/0          up          '
                           'up               ARPA  1514    1000000\n'}
---- napalm_configure ** changed : True ---------------------------------------- INFO
--- 
+++ 
@@ -66,6 +66,8 @@
 interface Loopback0
  description PRIMARY ROUTER
+!
+interface Loopback1000
 !
 interface MgmtEth0/RP0/CPU0/0
  description *** MANAGEMENT INTERFACE ***
---- napalm_get ** changed : False --------------------------------------------- INFO
{ 'interfaces': { 'Loopback0': { 'description': 'PRIMARY ROUTER ',
                                 'is_enabled': True,
                                 'is_up': True,
                                 'last_flapped': -1.0,
                                 'mac_address': '',
                                 'mtu': 1500,
                                 'speed': 0},
                  'Loopback1000': { 'description': '',
                                    'is_enabled': True,
                                    'is_up': True,
                                    'last_flapped': -1.0,
                                    'mac_address': '',
                                    'mtu': 1500,
                                    'speed': 0},
                  'MgmtEth0/RP0/CPU0/0': { 'description': '*** MANAGEMENT '
                                                          'INTERFACE ***',
                                           'is_enabled': True,
                                           'is_up': True,
                                           'last_flapped': -1.0,
                                           'mac_address': '52:54:00:A4:14:09',
                                           'mtu': 1514,
                                           'speed': 1000}}}
^^^^ END multiple_tasks ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* rt2 ** changed : True ********************************************************
vvvv multiple_tasks ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- napalm_cli ** changed : False --------------------------------------------- INFO
{ 'show interfaces brief': 'Intf       Intf        LineP              Encap  '
                           'MTU        BW\n'
                           '               Name       State       '
                           'State               Type (byte)    (Kbps)\n'
                           '--------------------------------------------------------------------------------\n
                           '               Lo10          up          '
                           'up           Loopback  1500          0\n'
                           '     Mg0/RP0/CPU0/0          up          '
                           'up               ARPA  1514          0\n'}
---- napalm_configure ** changed : True ---------------------------------------- INFO
--- 
+++ 
@@ -61,6 +61,8 @@
 !
 interface Loopback10
  description LOOPBACK 10
+!
+interface Loopback1000
 !
 interface MgmtEth0/RP0/CPU0/0
  description *** MANAGEMENT INTERFACE ***
---- napalm_get ** changed : False --------------------------------------------- INFO
{ 'interfaces': { 'Loopback10': { 'description': 'LOOPBACK 10',
                                  'is_enabled': True,
                                  'is_up': True,
                                  'last_flapped': -1.0,
                                  'mac_address': '',
                                  'mtu': 1500,
                                  'speed': 0},
                  'Loopback1000': { 'description': '',
                                    'is_enabled': True,
                                    'is_up': True,
                                    'last_flapped': -1.0,
                                    'mac_address': '',
                                    'mtu': 1500,
                                    'speed': 0},
                  'MgmtEth0/RP0/CPU0/0': { 'description': '*** MANAGEMENT '
                                                          'INTERFACE ***',
                                           'is_enabled': True,
                                           'is_up': True,
                                           'last_flapped': -1.0,
                                           'mac_address': '52:54:00:DE:B5:58',
                                           'mtu': 1514,
                                           'speed': 0}}}
^^^^ END multiple_tasks ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
The output shows the result of `show interfaces brief`, does the configuration of adding `interface loopback 1000` and shows the configuration changes before commiting it, then it retrieves interfaces information from the napalm interfaces getter method. These 3 tasks are executed on all the hosts provided in the hosts.yaml file. For every host the tasks are executed separately by a thread, hence the results are shown per host. 

#### Example 4

**Execute multiple napalm tasks on the selected hosts from the inventory, using the filter.**

```
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
```

This is same as Example 3, the only difference is, we are applying filter to the nornir object so that it executes all the tasks on a specific host of the inventory that is provided in the filter. 

Execute **nornir_main.py** file and retrieve the results.
```
./nornir_main.py
```
**Output**
```
multiple_tasks******************************************************************
* rt1 ** changed : True ********************************************************
vvvv multiple_tasks ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
---- napalm_cli ** changed : False --------------------------------------------- INFO
{ 'show interfaces brief': 'Intf       Intf        LineP              Encap  '
                           'MTU        BW\n'
                           '               Name       State       '
                           'State               Type (byte)    (Kbps)\n'
                           '--------------------------------------------------------------------------------\n'
                           '                Lo0          up          '
                           'up           Loopback  1500          0\n'
                           '     Mg0/RP0/CPU0/0          up          '
                           'up               ARPA  1514    1000000\n'}
---- napalm_configure ** changed : True ---------------------------------------- INFO
--- 
+++ 
@@ -66,6 +66,8 @@
 interface Loopback0
  description PRIMARY ROUTER
+!
+interface Loopback1000
 !
 interface MgmtEth0/RP0/CPU0/0
  description *** MANAGEMENT INTERFACE ***
---- napalm_get ** changed : False --------------------------------------------- INFO
{ 'interfaces': { 'Loopback0': { 'description': 'PRIMARY ROUTER ',
                                 'is_enabled': True,
                                 'is_up': True,
                                 'last_flapped': -1.0,
                                 'mac_address': '',
                                 'mtu': 1500,
                                 'speed': 0},
                  'Loopback1000': { 'description': '',
                                    'is_enabled': True,
                                    'is_up': True,
                                    'last_flapped': -1.0,
                                    'mac_address': '',
                                    'mtu': 1500,
                                    'speed': 0},
                  'MgmtEth0/RP0/CPU0/0': { 'description': '*** MANAGEMENT '
                                                          'INTERFACE ***',
                                           'is_enabled': True,
                                           'is_up': True,
                                           'last_flapped': -1.0,
                                           'mac_address': '52:54:00:A4:14:09',
                                           'mtu': 1514,
                                           'speed': 1000}}}
^^^^ END multiple_tasks ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
```
Though there are 2 hosts available in the inventory, the output shows the result of executed tasks on only one host i.e. `rt1`, as we have added a filter to do so.

## Conclusion
Nornir is a python based multi-threaded network automation framework that provides a way to automate your network tasks efficiently. Being an open-sourced project written in python makes it easy for the user to debug and troubleshoot. Above all, it's time-efficient, free, and easy to use. Write simple lines of python code to execute your network tasks on a lot of your network devices quickly!! 


## Resources

- [Nornir Documentation](https://nornir.readthedocs.io/en/latest/)
- [Nornir GitHub repository](https://github.com/nornir-automation/nornir)

