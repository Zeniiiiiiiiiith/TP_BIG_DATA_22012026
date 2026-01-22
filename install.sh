#!/usr/bin/env bash
set -euo pipefail

if [ ! -f .env ]; then
  echo "[INFO] .env not found. Copying from .env.example..."
  cp .env.example .env
  echo "[WARN] Please edit .env (AIRFLOW keys etc.)."
fi

echo "[INFO] Starting core platform..."
docker compose up -d --build minio zookeeper kafka minio-init kafka-init trino spark-master spark-worker airflow-db airflow filebeat

echo "[INFO] Core is up."
echo "MinIO Console:   http://localhost:9001  (${MINIO_ROOT_USER}/${MINIO_ROOT_PASSWORD} from .env)"
echo "Kafka:           localhost:9092"
echo "Airflow:         http://localhost:8088"
echo "Trino:           http://localhost:8082"
echo "Spark UI:        http://localhost:8080"

echo ""
echo "[INFO] Optional profiles:"
echo "  docker compose --profile obs up -d"
echo "  docker compose --profile ml  up -d --build"
