from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

spark = SparkSession.builder.appName("batch-csv-to-silver").getOrCreate()

src = "file:/data/csv/intrusion_labeled.csv"
bronze = "s3a://lakehouse/bronze/intrusion_csv/"
silver = "s3a://lakehouse/silver/intrusion_events/"

df = (spark.read.option("header", True).csv(src)
      .withColumn("ingest_ts", current_timestamp()))

# Write Bronze (raw)
df.write.mode("append").parquet(bronze)

# Silver (structuré)
df.write.mode("append").parquet(silver)

print("OK")
