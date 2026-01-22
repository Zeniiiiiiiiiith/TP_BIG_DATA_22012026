# TP Atelier Big Data 

- Conception de l'architecture du projet dans architecture.drawio.png

- Tout fonctionne jusqu'à l'entraînement du modèle sur Spark mais sans écriture de table dans Iceberg.

- Prometheus & Grafana ont des conteneurs mais actuellement aucun dashboard adapté au projet n'a été créé.

# How to use:

Démarrer le projet à la racine:

```
docker compose up -d
```

Vérifier que tout run correctement:

```
docker compose ps
```

Envoyer la data du CSV vers MinIO:

```
docker run --rm --network container:bigdataarch-minio-1 `
  -v mc-config:/root/.mc `
  -v "${PWD}:/work" `
  minio/mc:latest `
  cp /work/Network_logs.csv local/lakehouse/raw/network_logs/Network_logs.csv
```

Vérifier que le fichier est bien présent:
```
docker run --rm --network container:bigdataarch-minio-1 \
  -v mc-config:/root/.mc \
  minio/mc:latest ls local/lakehouse/raw/network_logs/
```

Process la data avec Trino & Iceberg:
```
docker compose exec trino trino
```

Créer une table externe en csv:
```
CREATE TABLE hive.raw.network_logs_raw (
  source_ip VARCHAR,
  destination_ip VARCHAR,
  port VARCHAR,
  request_type VARCHAR,
  protocol VARCHAR,
  payload_size VARCHAR,
  user_agent VARCHAR,
  status VARCHAR,
  intrusion VARCHAR,
  scan_type VARCHAR
)
WITH (
  format = 'CSV',
  external_location = 's3a://lakehouse/raw/network_logs/',
  skip_header_line_count = 1
);
```

Créer une table Iceberg:
```
CREATE TABLE iceberg.demo.network_logs_clean
WITH (format='PARQUET') AS
SELECT
  source_ip,
  destination_ip,
  CAST(port AS INTEGER) AS port,
  request_type,
  protocol,
  CAST(payload_size AS INTEGER) AS payload_size,
  user_agent,
  status,
  CAST(intrusion AS INTEGER) AS intrusion,
  scan_type
FROM hive.raw.network_logs_raw;
```

Créer la vue ML-ready:
```
CREATE OR REPLACE VIEW iceberg.demo.network_logs_ml AS
SELECT
  source_ip,
  destination_ip,
  port,
  request_type,
  protocol,
  payload_size,
  user_agent,
  status,
  scan_type,
  intrusion AS label
FROM iceberg.demo.network_logs_clean;
```

Entrainer le modèle avec Spark:

```
docker compose exec spark-master bash
```

Arrêter le projet:
```
docker compose down
```

Retirer tous les volumes:
```
docker compose down -v
```