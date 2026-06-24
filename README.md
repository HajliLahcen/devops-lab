# DevOps Lab - Banking Application

## Overview

This project is a complete DevOps lab built from scratch to learn modern DevOps practices and technologies.

The application simulates a simple banking system where users can:

* View account balances
* Transfer money between accounts
* Monitor infrastructure and application metrics

The platform is fully containerized using Docker and Docker Compose.

---

## Architecture

Frontend (Nginx)
↓
API (Python)
↓
PostgreSQL

Prometheus
↓
Grafana

Node Exporter
↓
Prometheus

---

## Technologies Used

### Application

* Python 3
* PostgreSQL 16
* HTML/CSS/JavaScript
* Nginx

### Containers

* Docker
* Docker Compose

### Monitoring

* Prometheus
* Grafana
* Node Exporter

### Version Control

* Git
* GitHub

---

## Project Structure

```text
devops-lab/
│
├── api/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── Dockerfile
│   └── transfer.html
│
├── monitoring/
│   ├── prometheus/
│   │   ├── Dockerfile
│   │   └── prometheus.yml
│   │
│   └── grafana/
│       └── Dockerfile
│
├── docker-compose.yml
│
└── README.md
```

---

## Services

| Service    | Port |
| ---------- | ---- |
| Frontend   | 8001 |
| API        | 8000 |
| PostgreSQL | 5432 |
| Prometheus | 9090 |
| Grafana    | 3000 |

---

## Build and Run

Start all services:

```bash
docker compose up -d --build
```

Check running services:

```bash
docker compose ps
```

Stop all services:

```bash
docker compose down
```

---

## Database Persistence

PostgreSQL data is stored using Docker Volumes.

This ensures database data remains available even if containers are recreated.

---

## Monitoring

### Prometheus

Prometheus collects metrics from:

* Prometheus Server
* Node Exporter

Access:

http://localhost:9090

### Grafana

Grafana visualizes metrics collected by Prometheus.

Access:

http://localhost:3000

---

## Future Roadmap

### Completed

* Docker
* Docker Compose
* PostgreSQL Migration
* Prometheus Monitoring
* Grafana Dashboards

---

## Author

Lahcen Hajli



DevOps / Cloud Engineering Lab Project
