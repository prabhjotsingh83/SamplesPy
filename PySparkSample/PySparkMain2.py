from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("MacBookTest") \
    .master("local[*]") \
    .getOrCreate()

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