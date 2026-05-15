from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SparkApp Prabh").getOrCreate()
df = spark.read.csv("../data/stocks.csv", header=True)

df.show()
print(df.count())
print(df.columns)