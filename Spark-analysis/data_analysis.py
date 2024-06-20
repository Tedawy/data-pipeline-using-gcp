#!/usr/bin/env python


# Create SparkSession from builder
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace,cast,trim
from pyspark.sql.functions import split, col,expr,when
import warnings
warnings.filterwarnings("ignore")

# Create a spark session 
spark = SparkSession.builder \
                .master('yarn') \
                .appName('de-capstone-project') \
                .config('spark.jars.packages', 'com.google.cloud.spark:spark-bigquery-with-dependencies_2.12:0.27.0') \
                .getOrCreate()


# Load the data from the google storage
df = spark.read.csv('gs://de-zoomcamp-bucket-1/2024-05-21/*', inferSchema=True , header=True, multiLine=True) 

# Show the first rows
df.show(5)

# Show the data types of the columns 
df.printSchema()


## Data Cleaning

# Drop duplicates values 
df = df.dropDuplicates()


# ### AREA 

# Clean area column
df = df.withColumn("area", regexp_replace("area", ",", ""))
df = df.withColumn("area", regexp_replace("area", " sqft", "").cast("int"))


# ### PROPERTY TYPE

# Define valid property types to keep
valid_property_types = [
    "Apartment", "Villa", "Townhouse", "Penthouse", 
    "Hotel Apartment", "Residential Building", "Residential Floor", "Villa Compound"
]

# Filter DataFrame to keep only valid property types
df = df.filter(df["property_type"].isin(valid_property_types))


# Show the number of different property types 
df.groupby('property_type').count().orderBy(col('count').desc()).show()


# ### BEDROOM
# Show number of diiferent bedrroms 
df.groupby('bedrooms').count().show()

### Values have sqft are |Residential Building and Residential Floor

# Replace sqft values of bedrooms by 0 bedrooms
df = df.withColumn('bedrooms', when(col("bedrooms").contains("sqft"), 0).otherwise(col("bedrooms")))

df.groupby('bedrooms').count().orderBy(col('count').desc()).show()

# Define valid bedrooms number to keep
valid_bedrooms_number = [
    0, "Studio", "1 Bed", "2 Beds", "3 Beds", "4 Beds","5 Beds"
    "6 Beds", "7 Beds", "8 Beds", "9 Beds", "10 Beds","11 Beds"
]

# Filter DataFrame to keep only valid bedrooms number
df = df.filter(df["bedrooms"].isin(valid_bedrooms_number))

df.groupby('bedrooms').count().orderBy(col('count').desc()).show()

# Clean bedrooms column 
df = df.withColumn("bedrooms",regexp_replace("bedrooms","(Beds|Bed)",""))

df.groupby('bedrooms').count().orderBy(col('count').desc()).show()

# ### BATHROOMS
df.groupby('bathrooms').count().show()

# Clean bathrooms column 
df = df.withColumn("bathrooms",trim(regexp_replace("bathrooms", "(Baths|Bath)","")))

df = df.filter(df['bathrooms'].isin(list(range(1,12))))

df.groupby('bathrooms').count().orderBy(col("count").desc()).show()

# ### PRICE

# Clean the price column and convert to integer 
df= df.withColumn("price",regexp_replace("price", ",","").cast("int"))

df.select('price').describe().show()

df.filter(df['price'] == 2000000000).show()


# ### LONGITUDE, LATITUDE

# Convert the columns latitude, longitude to float 
df = df.withColumn("latitude", df["latitude"].cast("float"))
df = df.withColumn("longitude", df["longitude"].cast("float"))


# ### LOCATION

# split the location column and create a column for district 
df = df.withColumn('location', split(df['location'], ', '))
df = df.withColumn('district', trim(expr("location[size(location) - 2]")))
df = df.drop('location')

# property types 
df.groupBy('district').count().show(30)

# ### FURNISHING

# Check values in furnishing
df.groupby('furnishing').count().show()

# Replace null values by 0 
df = df.withColumn('furnishing', when(df['furnishing'].isNull(),'Unknown').otherwise(df['furnishing']))

df.groupby('furnishing').count().show()


# ### COMPLETION STATUS

# Check values in completion_status
df.groupby('completion_status').count().show()

# Check null values in latitude and longitude and drop these values
(df.filter(col('longitude').isNull()).count(),  df.filter(col('latitude').isNull()).count())

# Drop Null values 
df = df.dropna(subset=['price','area', 'longitude','latitude'])

# Cleaned Dataframe 
cleaned_df = df.select(['area','bathrooms','bedrooms','longitude','latitude','completion_status','furnishing',\
                       'property_type','district','price'])

cleaned_df.show(5)

# Save the data to bucket
cleaned_df.write.parquet('gs://de-zoomcamp-bucket-1/clean_data', mode='overwrite')

# Stop the spark session
spark.stop()




