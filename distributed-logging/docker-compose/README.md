# Docker Compose

This `docker-compose.yml` file contains these images:

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

## How to use

You can simply run `docker compose up -d` in your terminal, docker will automatically download and configure everything necessary