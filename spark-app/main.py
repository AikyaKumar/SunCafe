from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, DoubleType

spark = SparkSession.builder \
    .appName("WeatherProcessor") \
    .config("spark.mongodb.write.connection.uri", "mongodb://mongodb:27017/weather.sunlight") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType() \
    .add("location", StructType()
         .add("lat", FloatType())
         .add("lon", FloatType())) \
    .add("cloud_cover", DoubleType()) \
    .add("sunlight", StringType()) \
    .add("timestamp", DoubleType())

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "weather") \
    .option("startingOffsets", "latest") \
    .load()

json_df = df.selectExpr("CAST(value AS STRING)")
parsed_df = json_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

query = parsed_df.writeStream \
    .format("mongodb") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .outputMode("append") \
    .start()

query.awaitTermination()