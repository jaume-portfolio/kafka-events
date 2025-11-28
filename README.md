# Kafka Events Streaming

## Overview

This project is a Python Kafka pipeline that simulates user and purchase events. It demonstrates a full end-to-end streaming workflow: generating data, sending events to Kafka topics, and consuming them into PostgreSQL. Kafka UI is included for monitoring topics and messages.

---

## Features

- Random **user & purchase generators**  
- **Kafka producer** streams to `users` and `purchases`  
- **Kafka consumers** insert data into PostgreSQL  
- **Dockerized**: Kafka, Zookeeper, Kafka UI, PostgreSQL, Python app  
- **Concurrent streaming** using Python multiprocessing  
- Short message retention (`KAFKA_LOG_RETENTION_MS = 60s`)


## Setup Instructions

1. **Clone the repository and start the containers:**
```bash
git clone https://github.com/jaume-portfolio
cd kafka-events
docker compose down -v && docker compose up -d --build && docker compose logs -f app