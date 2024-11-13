# OpenF1 Time Series Modeling and Analysis

# Time Series

# Development Setup

`sudo curl -sSLf https://get.k0s.sh | sudo sh`

`minikube start`

## Install InfluxDB

```bash
cd infra/
terraform init
terraform plan
```

Verify the plan then apply the changes.

```bash
terrafomrm apply
```

Make influxdb available to localhost

Get node port on localhost
 
`kubectl get svc -n influxdb -o jsonpath="{.items[?(@.metadata.name=='influxdb')].spec.ports[0].nodePort}"`

`minikube service influxdb --url`

`localhost:<node port>`



