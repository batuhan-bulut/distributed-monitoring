# Helm Chart

This Helm Chart contains all necessary configurations for run the application(s) in your environment.

- **NGINX-otel**
	- act as reverse proxy and add traces to requests
- **Postgres**
	- Database for the project
- **Redis**
	- Caching the values
- **Tempo**
	- Storing the Traces
- **Otel Collector**
	- Collect all Otel data and distributes them
- **Grafana**
	- Dashboarding
- **Loki**
	- Logs
- **Frontend**
	- Application for Frontend
- **Backend**
  - Application for Frontend
- **Prometheus**
	- Metrics
- Config Files for services

## Requirements
- kubectl
- minikube (optional)

I preferred minikube to deploy this charts to my environment but you can choose any kubernetes environment.

## How to use

After you download the helm charts you can run this command:

    helm install <ReleaseName> .

It will create all the resources required for this project under the `monitoring` namespace, if you don't wanna use this namespace you can edit from Values.yaml