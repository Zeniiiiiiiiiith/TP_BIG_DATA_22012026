from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, current_timestamp, to_timestamp, regexp_extract
from pyspark.sql.types import StructType, StructField, StringType

spark = SparkSession.builder.appName("streaming-logs-to-lake").getOrCreate()

schema = StructType([
    StructField("message", StringType(), True),
    StructField("source_type", StringType(), True),
])

raw = (spark.readStream.format("kafka")
       .option("kafka.bootstrap.servers", "kafka:9092")
       .option("subscribe", "raw-logs")
       .option("startingOffsets", "latest")
       .load())

json_df = raw.select(from_json(col("value").cast("string"), schema).alias("j")).select("j.*")

parsed = (json_df
    .withColumn("ingest_ts", current_timestamp())
    .withColumn("ip", regexp_extract(col("message"), r"^(\S+)", 1))
    .withColumn("status", regexp_extract(col("message"), r"\" \s*(\d{3})\s", 1))
)

# Bronze: raw JSON payloads
bronze_path = "s3a://lakehouse/bronze/web_logs/"
silver_path = "s3a://lakehouse/silver/web_events/"

q1 = (json_df.writeStream
      .format("parquet")
      .option("path", bronze_path)
      .option("checkpointLocation", "s3a://lakehouse/_checkpoints/bronze_web_logs")
      .outputMode("append")
      .start())

# Silver: parsed events
q2 = (parsed.writeStream
      .format("parquet")
      .option("path", silver_path)
      .option("checkpointLocation", "s3a://lakehouse/_checkpoints/silver_web_events")
      .outputMode("append")
      .start())

spark.streams.awaitAnyTermination()
