# 🐳 Docker Guide

Run the Wallet API using Docker and Docker Compose.

## Prerequisites
- Docker 20.10+
- Docker Compose 2.0+
- Git

## Quick Start
```bash
git clone <repo-url>
cd wallet-api
./start.sh       # builds the image and runs docker-compose
```
The API becomes available at http://localhost:8080.

## Manual commands
To build and run manually:
```bash
docker build -t wallet-api .
docker-compose up
```
Stop containers with:
```bash
docker-compose down
```

## MongoDB initialization
MongoDB is started with a container and initialized using the script in `docker/mongo-init/01-init-database.js`.

## Cleanup
```bash
docker system prune -f
```
