import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

class TestPipeline(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder \
            .appName("Pipeline_Tests") \
            .master("local[2]") \
            .config("spark.driver.memory", "2g") \
            .getOrCreate()
        
        cls.spark.sparkContext.setLogLevel("ERROR")
    
    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
    
    def test_spark_session(self):
        self.assertIsNotNone(self.spark)
        self.assertEqual(self.spark.sparkContext.appName, "Pipeline_Tests")
    
    def test_schema_definition(self):
        schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("price", IntegerType(), True),
            StructField("postcode", StringType(), True)
        ])
        
        self.assertEqual(len(schema.fields), 3)
        self.assertEqual(schema.fields[0].name, "transaction_id")
    
    def test_data_loading(self):
        data = [
            ("{123}", 200000, "SW1A 1AA"),
            ("{456}", 350000, "E1 6AN")
        ]
        
        schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("price", IntegerType(), True),
            StructField("postcode", StringType(), True)
        ])
        
        df = self.spark.createDataFrame(data, schema)
        
        self.assertEqual(df.count(), 2)
        self.assertEqual(len(df.columns), 3)
    
    def test_price_filtering(self):
        from pyspark.sql.functions import col
        
        data = [
            (100000,), (500000,), (1000000,), (15000000,)
        ]
        
        schema = StructType([StructField("price", IntegerType(), True)])
        df = self.spark.createDataFrame(data, schema)
        
        filtered = df.filter((col("price") > 0) & (col("price") < 10000000))
        
        self.assertEqual(filtered.count(), 3)
    
    def test_feature_creation(self):
        from pyspark.sql.functions import year, month, lit, to_date
        
        data = [("2023-01-15",), ("2023-06-20",)]
        schema = StructType([StructField("date_str", StringType(), True)])
        
        df = self.spark.createDataFrame(data, schema)
        df = df.withColumn("date", to_date(col("date_str"), "yyyy-MM-dd"))
        df = df.withColumn("year", year("date"))
        df = df.withColumn("month", month("date"))
        
        result = df.collect()
        
        self.assertEqual(result[0]['year'], 2023)
        self.assertEqual(result[0]['month'], 1)
        self.assertEqual(result[1]['month'], 6)
    
    def test_aggregation(self):
        from pyspark.sql.functions import avg, count
        
        data = [
            ("F", 200000),
            ("F", 250000),
            ("T", 300000),
            ("T", 350000)
        ]
        
        schema = StructType([
            StructField("property_type", StringType(), True),
            StructField("price", IntegerType(), True)
        ])
        
        df = self.spark.createDataFrame(data, schema)
        
        agg_df = df.groupBy("property_type").agg(
            avg("price").alias("avg_price"),
            count("*").alias("count")
        )
        
        results = {row['property_type']: row['avg_price'] for row in agg_df.collect()}
        
        self.assertEqual(results['F'], 225000)
        self.assertEqual(results['T'], 325000)
    
    def test_null_handling(self):
        from pyspark.sql.functions import col, when
        
        data = [(None,), (100000,), (None,), (200000,)]
        schema = StructType([StructField("price", IntegerType(), True)])
        
        df = self.spark.createDataFrame(data, schema)
        
        non_null = df.filter(col("price").isNotNull())
        
        self.assertEqual(non_null.count(), 2)
    
    def test_string_indexing(self):
        from pyspark.ml.feature import StringIndexer
        
        data = [("F",), ("T",), ("F",), ("D",)]
        schema = StructType([StructField("property_type", StringType(), True)])
        
        df = self.spark.createDataFrame(data, schema)
        
        indexer = StringIndexer(inputCol="property_type", outputCol="property_index")
        model = indexer.fit(df)
        indexed = model.transform(df)
        
        self.assertIn("property_index", indexed.columns)
        self.assertEqual(indexed.count(), 4)

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPipeline)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
