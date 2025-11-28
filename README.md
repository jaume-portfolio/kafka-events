# Kafka Events Streaming

## Overview

This project is a Python Kafka pipeline that simulates user and purchase events. It demonstrates a full end-to-end streaming workflow: generating data, sending events to Kafka topics, and consuming them into PostgreSQL. Kafka UI is included for monitoring topics and messages.

## Features

- Random **user & purchase generators**  
- **Kafka producer** streams to `users` and `purchases`  
- **Kafka consumers** insert data into PostgreSQL  
- **DLQ (Dead Letter Queue)** for invalid or malformed user messages  
- **Dockerized**: Kafka, Zookeeper, Kafka UI, PostgreSQL, Python app  
- **Concurrent streaming** using Python multiprocessing  
- Short message retention (`KAFKA_LOG_RETENTION_MS = 60s`)



## Setup Instructions

1. **Clone the repository and start the containers:**
```bash
git clone https://github.com/jaume-portfolio/kafka-events
cd kafka-events
docker compose down -v && docker compose up -d --build && docker compose logs -f app
```

## Assumptions made
- Docker and Docker Compose are installed on the target machine.  
- PostgreSQL is used as the database backend for local testing.  
- Kafka messages are retained for 60 seconds for quick testing purposes.  
- Python scripts generate 100,000 users and purchase events by default.  
- Users and purchases are linked via `user_id`.  


## Infrastructure description

- Fully containerized using Docker and Docker Compose.  
- Services included:  
  - **Zookeeper**: Kafka coordination  
  - **Kafka broker**: Event streaming  
  - **Kafka UI**: Topic monitoring. Inspect messages at http://localhost:8080
  - **PostgreSQL**: Stores user and purchase events  
  - **Python app**: Generates events and runs consumers  


## Connecting to PostgreSQL

Use a client like **DataGrip**, **DBeaver**, or **pgAdmin**:

- **Host:** `localhost`  
- **Port:** `5432`  
- **Database:** `stream`  
- **User:** `postgres`  
- **Password:** `postgres`  

Find the tables in the schema stream_target
