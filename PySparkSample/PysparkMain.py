import os
import logging
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf

# Suppress Hadoop warnings
logging.getLogger("org.apache.hadoop").setLevel(logging.ERROR)
logging.getLogger("org.apache.spark").setLevel(logging.WARN)

# Clear any problematic Hadoop environment variables
for env_var in ['HADOOP_CONF_DIR', 'YARN_CONF_DIR', 'HADOOP_HOME']:
    if env_var in os.environ:
        del os.environ[env_var]

# Create Spark configuration
conf = SparkConf()
conf.setAppName("MacBookTest")
conf.setMaster("local[*]")
# Explicitly set filesystem configurations
conf.set("spark.hadoop.fs.defaultFS", "file:///")
conf.set("spark.sql.warehouse.dir", "file:///tmp/spark-warehouse")
conf.set("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem")
conf.set("spark.hadoop.fs.hdfs.impl", "org.apache.hadoop.fs.DistributedFileSystem")
# Disable ViewFS which is causing the error
conf.set("spark.hadoop.fs.viewfs.impl", "")
conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")

# Initialize Spark Session with the configuration
spark = SparkSession.builder.config(conf=conf).getOrCreate()

# Create sample data
data = [("Alice", 34), ("Bob", 45), ("Charlie", 29)]
columns = ["Name", "Age"]

# Create and display DataFrame
df = spark.createDataFrame(data, schema=columns)
df.show()

# Run a SQL query
df.createOrReplaceTempView("people")
result = spark.sql("SELECT * FROM people WHERE Age > 30")
result.show()

# Stop the session
spark.stop()