# Docker Deployment Guide

This guide provides comprehensive instructions for deploying and managing the CryptoHistoricalMarketData application using Docker.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Usage Examples](#usage-examples)
6. [Maintenance](#maintenance)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Topics](#advanced-topics)

## Overview

The Docker setup for this application provides:

- **Isolated Environment**: Consistent execution environment across different systems
- **Easy Deployment**: Simple setup with minimal configuration
- **Data Persistence**: Volume mounting for configuration and data
- **Reproducibility**: Versioned dependencies in requirements.txt

### Docker Architecture

```
Host System
├── ./ignore/              → /app/ignore (config volume)
├── ./app/Data/            → /app/app/Data (data volume)
└── Docker Container
    ├── Python 3.11 slim
    ├── Application code
    └── Python dependencies
```

## Prerequisites

### Required Software

- **Docker Engine**: Version 20.10 or later
  ```bash
  docker --version
  ```

- **Docker Compose**: V2 or later (comes with Docker Desktop)
  ```bash
  docker compose version
  ```

### Installation

**Linux:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group (optional, avoids sudo)
sudo usermod -aG docker $USER
newgrp docker
```

**macOS:**
- Install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)

**Windows:**
- Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/alunfes/CryptoHistoricalMarketData.git
cd CryptoHistoricalMarketData
```

### 2. Configure Settings

Edit configuration files in `ignore/` directory:

```bash
# Edit parameters
nano ignore/params.yaml

# Verify API endpoints (usually no changes needed)
nano ignore/apiendpoints.yaml
```

Example `params.yaml`:
```yaml
exchanges: ['bybit', 'okx', 'dydx', 'apexpro']
since_num_days_before: 90
ohlcv_data_interval:
  okx: '1m'
  bybit: 1
  dydx: '1MIN'
  apexpro: 1
```

### 3. Build and Start Container

```bash
# Build and start in detached mode
docker compose up --build -d

# Check container status
docker compose ps
```

### 4. Run Data Fetcher

```bash
# Execute data download
docker compose exec crypto-data-fetcher python3 app/main.py

# Or run in the background
docker compose exec -d crypto-data-fetcher python3 app/main.py
```

### 5. View Logs

```bash
# Follow logs in real-time
docker compose logs -f crypto-data-fetcher

# View last 100 lines
docker compose logs --tail=100 crypto-data-fetcher
```

## Configuration

### Environment Variables

You can customize behavior using environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - TZ=UTC  # Set timezone
```

### Volume Mounts

The setup uses two volume mounts:

1. **Configuration Volume** (read-only recommended):
   ```yaml
   - ./ignore:/app/ignore:ro
   ```

2. **Data Volume** (read-write):
   ```yaml
   - ./app/Data:/app/app/Data
   ```

### Custom Dockerfile Modifications

To customize the Docker image, edit `Dockerfile`:

```dockerfile
# Example: Change Python version
FROM python:3.12-slim

# Example: Add additional system packages
RUN apt-get update && apt-get install -y \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*
```

Then rebuild:
```bash
docker compose up --build
```

## Usage Examples

### One-time Execution

Run the data fetcher once and exit:

```bash
docker compose run --rm crypto-data-fetcher python3 app/main.py
```

### Interactive Shell

Access the container for debugging or manual operations:

```bash
docker compose exec crypto-data-fetcher /bin/bash

# Inside container
python3 app/main.py
python3 app/test.py
ls -la app/Data/
```

### Scheduled Execution

#### Using Host Cron

Create a cron job on the host system:

```bash
# Edit crontab
crontab -e

# Run every hour at minute 0
0 * * * * cd /path/to/CryptoHistoricalMarketData && docker compose exec -T crypto-data-fetcher python3 app/main.py >> /var/log/crypto_data.log 2>&1

# Run daily at 3 AM
0 3 * * * cd /path/to/CryptoHistoricalMarketData && docker compose exec -T crypto-data-fetcher python3 app/main.py >> /var/log/crypto_data.log 2>&1
```

#### Using Docker Compose with Modified Command

Edit `docker-compose.yml` to run continuously:

```yaml
command: |
  sh -c "while true; do
    python3 app/main.py
    sleep 3600  # Wait 1 hour
  done"
```

### Multiple Instances

Run multiple containers for different exchange configurations:

```yaml
# docker-compose.yml
services:
  crypto-bybit:
    build: .
    volumes:
      - ./ignore-bybit:/app/ignore
      - ./data-bybit:/app/app/Data
    command: python3 app/main.py

  crypto-okx:
    build: .
    volumes:
      - ./ignore-okx:/app/ignore
      - ./data-okx:/app/app/Data
    command: python3 app/main.py
```

## Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker compose down
docker compose up --build -d
```

### Backing Up Data

```bash
# Backup data directory
tar -czf crypto-data-backup-$(date +%Y%m%d).tar.gz app/Data/

# Or use rsync
rsync -av app/Data/ /backup/location/
```

### Cleaning Up

```bash
# Stop and remove containers
docker compose down

# Remove containers and volumes
docker compose down -v

# Remove Docker images
docker rmi crypto-data-fetcher

# Clean up Docker system
docker system prune -a
```

### Viewing Container Resource Usage

```bash
# Real-time stats
docker stats crypto-historical-data

# Container details
docker compose ps
docker inspect crypto-historical-data
```

## Troubleshooting

### Container Won't Start

1. **Check logs:**
   ```bash
   docker compose logs crypto-data-fetcher
   ```

2. **Verify configuration:**
   ```bash
   docker compose config
   ```

3. **Check port conflicts:**
   ```bash
   docker compose ps
   ```

### Permission Issues

If you encounter permission issues with mounted volumes:

```bash
# Check ownership
ls -la app/Data/

# Fix permissions (Linux/Mac)
sudo chown -R $USER:$USER app/Data/
chmod -R 755 app/Data/

# Or run container as current user
docker compose run --user $(id -u):$(id -g) crypto-data-fetcher python3 app/main.py
```

### Network Issues

If APIs are unreachable:

```bash
# Test from container
docker compose exec crypto-data-fetcher curl -I https://indexer.dydx.trade/v4/perpetualMarkets

# Check DNS resolution
docker compose exec crypto-data-fetcher nslookup indexer.dydx.trade
```

### Out of Memory

Increase Docker memory limit:

**Docker Desktop:**
- Settings → Resources → Memory

**Command line:**
```bash
docker compose run --memory="2g" crypto-data-fetcher python3 app/main.py
```

### Build Failures

Clear build cache and rebuild:

```bash
docker compose build --no-cache
docker compose up
```

## Advanced Topics

### Production Deployment

#### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml crypto-stack

# Scale service
docker service scale crypto-stack_crypto-data-fetcher=3
```

#### Using Kubernetes

Create a Kubernetes deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crypto-data-fetcher
spec:
  replicas: 1
  selector:
    matchLabels:
      app: crypto-data-fetcher
  template:
    metadata:
      labels:
        app: crypto-data-fetcher
    spec:
      containers:
      - name: crypto-data-fetcher
        image: crypto-data-fetcher:latest
        volumeMounts:
        - name: config
          mountPath: /app/ignore
        - name: data
          mountPath: /app/app/Data
      volumes:
      - name: config
        configMap:
          name: crypto-config
      - name: data
        persistentVolumeClaim:
          claimName: crypto-data-pvc
```

#### Using Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: crypto-data-fetcher
spec:
  schedule: "0 * * * *"  # Every hour
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: crypto-data-fetcher
            image: crypto-data-fetcher:latest
            command: ["python3", "app/main.py"]
            volumeMounts:
            - name: config
              mountPath: /app/ignore
            - name: data
              mountPath: /app/app/Data
          restartPolicy: OnFailure
          volumes:
          - name: config
            configMap:
              name: crypto-config
          - name: data
            persistentVolumeClaim:
              claimName: crypto-data-pvc
```

### Health Checks

Add health check to `docker-compose.yml`:

```yaml
services:
  crypto-data-fetcher:
    healthcheck:
      test: ["CMD", "python3", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Multi-stage Builds

Optimize image size with multi-stage build:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app/ /app/app/
COPY ignore/ /app/ignore/
ENV PATH=/root/.local/bin:$PATH
CMD ["python3", "app/main.py"]
```

### Monitoring and Logging

#### Using Docker Logging Driver

```yaml
services:
  crypto-data-fetcher:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

#### Using External Logging Service

```yaml
services:
  crypto-data-fetcher:
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://192.168.0.42:514"
```

### Security Best Practices

1. **Run as non-root user:**
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

2. **Use read-only root filesystem:**
   ```yaml
   security_opt:
     - no-new-privileges:true
   read_only: true
   tmpfs:
     - /tmp
   ```

3. **Limit resources:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 1G
       reservations:
         memory: 512M
   ```

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Main README](README.md)
- [Japanese README](README_ja.md)

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review container logs: `docker compose logs`
3. Create an issue on GitHub with logs and configuration details
