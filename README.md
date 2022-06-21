## Installation
Install Python 3.6 or later, if you dont already have it.

## Install Locust:

```bash
pip3 install locust
```

Validate your installation. If this doesnt work, check the wiki for some possible solutions.

```bash
locust -V
locust 2.5.1
```
## How to Run Locust in local
Run command line

```bash
locust -f tasks/test-api.py
```

## How to create new test cases ?
Please refer to ```environments/``` and ```tasks/```. Find more locust documentations in https://locust.io/

## Running Locust docker locally (standalone mode)
```bash
docker run --rm -it -v /host_ABSOLUTE_directory/locust/tasks:/locust-tasks -e "TARGET_HOST=http://TARGET_HOST" -e "LOCUST_SCRIPT=/locust-tasks/TARGET_SCRIPT.py" -p 8089:8089 greenbirdit/locust
```

## Distributed load generation
A single process running Locust can simulate a reasonably high throughput. For a simple test plan it should be able to make many hundreds of requests per second, thousands if you use FastHttpUser.

But if your test plan is complex or you want to run even more load, you’ll need to scale out to multiple processes, maybe even multiple machines.

To do this, you start one instance of Locust in master mode using the ```--master``` flag and multiple worker instances using the ```--worker``` flag. If the workers are not on the same machine as the master you use ```--master-host``` to point them to the IP/hostname of the machine running the master.

The master instance runs Locust’s web interface, and tells the workers when to spawn/stop Users. The workers run your Users and send back statistics to the master. The master instance doesn’t run any Users itself.

### Example
To start locust in master mode:
```bash
locust -f my_locustfile.py --master
```
And then on each worker (replace 192.168.0.14 with the IP of the master machine, or leave out the parameter altogether if your workers are on the same machine as the master):
```bash
locust -f my_locustfile.py --worker --master-host=192.168.0.14
```
[Reference](http://docs.locust.io/en/stable/running-locust-distributed.html)

## Locust Helm Chart

This is a templated deployment of [Locust](http://locust.io) for Distributed Load
testing using Kubernetes.

## Pre Requisites:

* Requires (and tested with) helm `v2.1.2` or above.

## Chart details

This chart will do the following:

* Convert all files in `tasks/` folder into a configmap
* If an existing configmap is specified, it will be used instead of building one from the chart
* Create a Locust master and Locust worker deployment with the Target host
  and Tasks file specified.


### Installing the chart

To install the chart with the release name `locust-nymph` in the default namespace:

```bash
helm install -n locust-nymph --set master.config.target-host=http://site.example.com stable/locust
```

| Parameter                    | Description                             | Default                                               |
| ---------------------------- | ----------------------------------      | ----------------------------------------------------- |
| `Name`                       | Locust master name                      | `locust`                                              |
| `image.repository`           | Locust container image name             | `greenbirdit/locust`                                  |
| `image.tag`                  | Locust Container image tag              | `0.9.0`                                               |
| `image.pullSecrets`          | Locust Container image registry secret  | `None`                                                |
| `service.type`               | k8s service type exposing master        | `NodePort`                                            |
| `service.nodePort`           | Port on cluster to expose master        | `0`                                                   |
| `service.annotations`        | KV containing custom annotations        | `{}`                                                  |
| `service.extraLabels`        | KV containing extra labels              | `{}`                                                  |
| `extraVolumes`               | List of extra Volumes                   | `[]`                                                  |
| `extraVolumeMounts`          | List of extra Volume Mounts             | `[]`                                                  |
| `extraEnvs`                  | List of extra Environment Variables     | `[]`                                                  |
| `master.config.target-host`  | locust target host                      | `http://site.example.com`                             |
| `master.nodeSelector`        | k8s nodeselector                        | `{}`                                                  |
| `master.tolerations`         | k8s tolerance                           | `{}`                                                  |
| `worker.config.locust-script`| locust script to run                    | `/locust-tasks/tasks.py`                              |
| `worker.config.configmapName`| configmap to mount locust scripts from  | `empty, configmap is created from tasks folder in Chart` |
| `worker.replicaCount`        | Number of workers to run                | `2`                                                   |
| `worker.nodeSelector`        | k8s nodeselector                        | `{}`                                                  |
| `worker.tolerations`         | k8s tolerance                           | `{}`                                                  |

Specify parameters using `--set key=value[,key=value]` argument to `helm install`

Alternatively a YAML file that specifies the values for the parameters can be provided like this:

```bash
$ helm install --name my-release -f values.yaml stable/locust
```

#### Creating configmap with your Locust task files

You're probably developing your own Locust scripts that you want to run in this distributed setup.
To get those scripts into this deployment you can fork the chart and put them into the `tasks` folder. From there
they will be converted to a configmap and mounted for use in Locust.

Another solution, if you don't want to fork the Chart, is to put your Locust scripts in a configmap and provide the name
as a config parameter in `values.yaml`. You can read more on the use of configmaps as volumes in pods [here](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/).

If you have your Locust task files in a folder named "scripts" you would use something like the following command:

`kubectl create configmap locust-worker-configs --from-file path/to/scripts`


### Interacting with Locust

Get the Locust URL following the Post Installation notes. Using port forwarding you should be able to connect to the
web ui on Locust master node.

You can start the swarm from the command line using port forwarding as follows:

for example:
```bash
export LOCUST_URL=http://127.0.0.1:8089
```

Start / Monitor & Stop the Locust swarm via the web panel or with following commands:

Start:
```bash
curl -XPOST $LOCUST_URL/swarm -d"locust_count=100&hatch_rate=10"
```

Monitor:
```bash
watch -n 1 "curl -s $LOCUST_URL/stats/requests | jq -r '[.user_count, .total_rps, .state] | @tsv'"
```

Stop:
```bash
curl $LOCUST_URL/stop
```
