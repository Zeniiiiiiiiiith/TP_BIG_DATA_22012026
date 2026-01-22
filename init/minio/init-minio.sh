#!/bin/sh
set -e

mc alias set local http://minio:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

# Buckets lakehouse
mc mb -p local/lakehouse || true
mc mb -p local/mlflow-artifacts || true

# Bronze/Silver/Gold folders (convention)
mc cp --recursive /dev/null local/lakehouse/bronze/ 2>/dev/null || true
mc cp --recursive /dev/null local/lakehouse/silver/ 2>/dev/null || true
mc cp --recursive /dev/null local/lakehouse/gold/   2>/dev/null || true

echo "[MINIO] Buckets ready: lakehouse, mlflow-artifacts"
