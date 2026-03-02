import os
import sys
import time
import yaml
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class PropertyPricePipeline:
    def __init__(self, config_path='../config/spark_config.yaml'):
        self.config = self.load_config(config_path)
        self.spark = self.initialize_spark()
        self.start_time = time.time()
        
    def load_config(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return self.default_config()
    
    def default_config(self):
        return {
            'spark': {
                'app_name': 'Property_Price_Pipeline',
                'driver_memory': '8g',
                'executor_memory': '8g',
                'shuffle_partitions': 200
            },
            'data': {
                'input_path': '../land_registry_data/merged_land_registry.csv',
                'output_path': '../data/property_prices.parquet'
            }
        }
    
    def initialize_spark(self):
        spark_config = self.config.get('spark', {})
        spark = SparkSession.builder \
            .appName(spark_config.get('app_name', 'Pipeline')) \
            .config("spark.driver.memory", spark_config.get('driver_memory', '8g')) \
            .config("spark.executor.memory", spark_config.get('executor_memory', '8g')) \
            .config("spark.sql.shuffle.partitions", spark_config.get('shuffle_partitions', 200)) \
            .config("spark.sql.adaptive.enabled", "true") \
            .getOrCreate()
        
        spark.sparkContext.setLogLevel("WARN")
        return spark
    
    def run_data_ingestion(self):
        print("="*60)
        print("Stage 1: Data Ingestion")
        print("="*60)
        
        from pyspark.sql.types import StructType, StructField, StringType, IntegerType
        from pyspark.sql.functions import col, to_date, year, month
        
        schema = StructType([
            StructField("transaction_id", StringType(), True),
            StructField("price", IntegerType(), True),
            StructField("date_of_transfer", StringType(), True),
            StructField("postcode", StringType(), True),
            StructField("property_type", StringType(), True),
            StructField("old_new", StringType(), True),
            StructField("duration", StringType(), True),
            StructField("paon", StringType(), True),
            StructField("saon", StringType(), True),
            StructField("street", StringType(), True),
            StructField("locality", StringType(), True),
            StructField("town_city", StringType(), True),
            StructField("district", StringType(), True),
            StructField("county", StringType(), True),
            StructField("ppd_category", StringType(), True),
            StructField("record_status", StringType(), True)
        ])
        
        input_path = self.config['data']['input_path']
        print(f"Loading data from: {input_path}")
        
        df = self.spark.read \
            .option("header", "true") \
            .schema(schema) \
            .csv(input_path)
        
        df = df.withColumn("date_of_transfer", to_date(col("date_of_transfer"), "yyyy-MM-dd"))
        df = df.withColumn("year", year("date_of_transfer"))
        df = df.withColumn("month", month("date_of_transfer"))
        
        count = df.count()
        print(f"Records loaded: {count:,}")
        
        output_path = self.config['data']['output_path']
        print(f"Saving to: {output_path}")
        
        df.write.mode("overwrite").partitionBy("year", "property_type").parquet(output_path)
        
        print("✓ Data ingestion completed\n")
        return df
    
    def run_feature_engineering(self):
        print("="*60)
        print("Stage 2: Feature Engineering")
        print("="*60)
        
        from pyspark.sql.functions import quarter, dayofweek, datediff, lit, when
        from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
        from pyspark.ml import Pipeline
        
        df = self.spark.read.parquet(self.config['data']['output_path'])
        print(f"Loaded {df.count():,} records")
        
        df = df.withColumn("quarter", quarter("date_of_transfer"))
        df = df.withColumn("day_of_week", dayofweek("date_of_transfer"))
        df = df.withColumn("days_since_2019", datediff(col("date_of_transfer"), lit("2019-01-01")))
        
        categorical_cols = ["property_type", "old_new", "duration"]
        indexers = [StringIndexer(inputCol=c, outputCol=c+"_index", handleInvalid="keep") 
                   for c in categorical_cols]
        encoders = [OneHotEncoder(inputCol=c+"_index", outputCol=c+"_encoded") 
                   for c in categorical_cols]
        
        numeric_features = ["year", "month", "quarter", "day_of_week", "days_since_2019"]
        encoded_features = [c+"_encoded" for c in categorical_cols]
        
        assembler = VectorAssembler(
            inputCols=numeric_features + encoded_features,
            outputCol="features_unscaled"
        )
        
        scaler = StandardScaler(inputCol="features_unscaled", outputCol="features")
        
        pipeline = Pipeline(stages=indexers + encoders + [assembler, scaler])
        
        print("Fitting feature pipeline...")
        model = pipeline.fit(df)
        
        print("Transforming data...")
        df_features = model.transform(df)
        df_features = df_features.withColumn("label", col("price"))
        
        df_features = df_features.filter(
            (col("price").isNotNull()) & 
            (col("price") > 0) & 
            (col("price") < 10000000)
        )
        
        output_path = "../data/processed_features.parquet"
        print(f"Saving features to: {output_path}")
        df_features.write.mode("overwrite").parquet(output_path)
        
        model.write().overwrite().save("../data/feature_pipeline_model")
        
        print("✓ Feature engineering completed\n")
        return df_features
    
    def run_model_training(self):
        print("="*60)
        print("Stage 3: Model Training")
        print("="*60)
        
        from pyspark.ml.regression import RandomForestRegressor
        from pyspark.ml.evaluation import RegressionEvaluator
        
        df = self.spark.read.parquet("../data/processed_features.parquet")
        print(f"Loaded {df.count():,} records")
        
        train_data = df.filter(col("year") <= 2022)
        test_data = df.filter(col("year") == 2023)
        
        print(f"Train: {train_data.count():,} | Test: {test_data.count():,}")
        
        rf = RandomForestRegressor(
            featuresCol="features",
            labelCol="label",
            numTrees=50,
            maxDepth=10,
            seed=42
        )
        
        print("Training Random Forest model...")
        start = time.time()
        model = rf.fit(train_data)
        train_time = time.time() - start
        
        print(f"Training completed in {train_time:.2f} seconds")
        
        predictions = model.transform(test_data)
        
        evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction")
        rmse = evaluator.evaluate(predictions, {evaluator.metricName: "rmse"})
        r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})
        mae = evaluator.evaluate(predictions, {evaluator.metricName: "mae"})
        
        print(f"\nModel Performance:")
        print(f"  RMSE: £{rmse:,.2f}")
        print(f"  R²: {r2:.4f}")
        print(f"  MAE: £{mae:,.2f}")
        
        model.write().overwrite().save("../data/models/random_forest")
        
        print("✓ Model training completed\n")
        return model
    
    def run_evaluation(self):
        print("="*60)
        print("Stage 4: Model Evaluation")
        print("="*60)
        
        from pyspark.ml.regression import RandomForestRegressionModel
        from pyspark.ml.evaluation import RegressionEvaluator
        import pandas as pd
        
        df = self.spark.read.parquet("../data/processed_features.parquet")
        test_data = df.filter(col("year") == 2023)
        
        model = RandomForestRegressionModel.load("../data/models/random_forest")
        
        predictions = model.transform(test_data)
        
        evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction")
        
        metrics = {
            'RMSE': evaluator.evaluate(predictions, {evaluator.metricName: "rmse"}),
            'R2': evaluator.evaluate(predictions, {evaluator.metricName: "r2"}),
            'MAE': evaluator.evaluate(predictions, {evaluator.metricName: "mae"}),
            'MSE': evaluator.evaluate(predictions, {evaluator.metricName: "mse"})
        }
        
        print("\nFinal Model Metrics:")
        for metric, value in metrics.items():
            if metric in ['RMSE', 'MAE', 'MSE']:
                print(f"  {metric}: £{value:,.2f}")
            else:
                print(f"  {metric}: {value:.4f}")
        
        results_df = pd.DataFrame([metrics])
        results_df.to_csv("../tableau/pipeline_results.csv", index=False)
        
        print("✓ Evaluation completed\n")
    
    def run(self):
        print("\n" + "="*60)
        print("UK PROPERTY PRICE PREDICTION PIPELINE")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        try:
            self.run_data_ingestion()
            self.run_feature_engineering()
            self.run_model_training()
            self.run_evaluation()
            
            elapsed = time.time() - self.start_time
            print("="*60)
            print(f"PIPELINE COMPLETED SUCCESSFULLY")
            print(f"Total Time: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ Pipeline failed: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        
        finally:
            self.spark.stop()

if __name__ == "__main__":
    pipeline = PropertyPricePipeline()
    pipeline.run()
