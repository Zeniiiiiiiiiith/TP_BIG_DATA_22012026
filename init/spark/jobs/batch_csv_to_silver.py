from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder.appName("batch-csv-to-silver").getOrCreate()

src = "file:/data/csv/intrusion_labeled.csv"
bronze = "s3a://lakehouse/bronze/intrusion_csv/"
silver = "s3a://lakehouse/silver/intrusion_events/"

df = (spark.read.option("header", True).csv(src)
      .withColumn("ingest_ts", current_timestamp()))

# Write Bronze (raw structured)
df.write.mode("append").parquet(bronze)

# Silver: enforce simple normalisation example
# (à adapter aux colonnes réelles : label, session_id, user_id, etc.)
df.write.mode("append").parquet(silver)

print("OK")
