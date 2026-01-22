#!/bin/sh
set -e

kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic raw-logs --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic parsed-events --partitions 1 --replication-factor 1
kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic alerts --partitions 1 --replication-factor 1

echo "[KAFKA] Topics created: raw-logs, parsed-events, alerts"
