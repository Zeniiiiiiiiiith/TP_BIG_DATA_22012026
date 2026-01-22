from datetime import timedelta
from feast import Entity, FeatureView, Field
from feast.types import Float32, Int64, String
from feast.data_source import FileSource

user = Entity(name="user_id", join_keys=["user_id"])

source = FileSource(
    path="data/gold_sessions.parquet",
    timestamp_field="event_ts",
)

session_features = FeatureView(
    name="session_features",
    entities=[user],
    ttl=timedelta(days=7),
    schema=[
        Field(name="pages", dtype=Int64),
        Field(name="errors", dtype=Int64),
        Field(name="risk_score", dtype=Float32),
    ],
    source=source,
)
