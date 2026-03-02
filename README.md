# UK Property Price Prediction - Big Data ML Project

A comprehensive big data machine learning project analyzing UK Land Registry property price data using PySpark MLlib, implementing distributed ML algorithms, scalability analysis, and interactive Tableau visualizations.

## Project Overview

This project applies foundational Big Data concepts within various Machine Learning algorithms to predict UK property prices. The analysis uses 1.1GB of real-world data (6.7M+ transactions from 2019-2025) and implements the complete ML pipeline using distributed computing frameworks.

### Dataset
- **Source**: UK Land Registry Price Paid Data
- **Size**: 1.1GB (6,721,312 records)
- **Time Period**: 2019-2025
- **Features**: 16 columns including price, location, property type, and transaction details

### Key Features
- Distributed data processing with PySpark
- 4+ ML algorithms (Linear Regression, Decision Trees, Random Forest, GBT)
- Hyperparameter tuning with cross-validation
- Scalability analysis (strong & weak scaling)
- Interactive Tableau dashboards
- Comprehensive performance optimization

## Project Structure

```
project/
├── notebooks/
│   ├── 1_data_ingestion.ipynb
│   ├── 2_feature_engineering.ipynb
│   ├── 3_model_training.ipynb
│   └── 4_evaluation.ipynb
├── scripts/
│   ├── run_pipeline.py
│   └── performance_profiler.py
├── tableau/
│   └── README_tableau.md
├── tests/
│   └── test_pipeline.py

└── README.md
```

## Technical Stack

- **Big Data**: Apache Spark 3.4.0, PySpark
- **ML Framework**: PySpark MLlib
- **Visualization**: Tableau Public, Matplotlib, Seaborn
- **Language**: Python 3.8+
- **Storage**: Parquet (columnar format)

## Installation & Setup

### Prerequisites
- Python 3.8+
- Java 8 or 11 (for Spark)
- 8GB+ RAM recommended

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd codespaces-blank
```

2. **Run setup script**
```bash
cd scripts
chmod +x setup_environment.sh
./setup_environment.sh
```

3. **Activate environment**
```bash
source venv/bin/activate
```

4. **Start Jupyter**
```bash
jupyter notebook
```


## Usage

### Running the Complete Pipeline

```bash
cd scripts
python run_pipeline.py
```

### Running Individual Notebooks

1. **Data Ingestion**: Load CSV, validate schema, convert to Parquet
2. **Feature Engineering**: Create temporal, location, and aggregated features
3. **Model Training**: Train 4 ML models with hyperparameter tuning
4. **Evaluation**: Comprehensive metrics, visualizations, and insights

### Running Tests

```bash
cd tests
python test_pipeline.py
```

## Data Processing Pipeline

### 1. Data Ingestion
- **Input**: 1.1GB CSV file
- **Processing**: Schema validation, type conversion, partitioning
- **Output**: Partitioned Parquet (by year & property_type)
- **Performance**: ~45 seconds load time

### 2. Feature Engineering
- **Temporal Features**: year, month, quarter, day_of_week
- **Location Features**: postcode_area, district aggregations
- **Aggregated Features**: area_avg_price, transaction_count
- **Encoding**: StringIndexer + OneHotEncoder
- **Scaling**: StandardScaler
- **Output**: Feature vectors ready for ML

### 3. Model Training
- **Algorithms**: 
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor (50 trees)
  - Gradient Boosted Trees (30 iterations)
- **Hyperparameter Tuning**: 3-fold cross-validation
- **Parallelism**: 4 parallel jobs
- **Model Persistence**: MLlib format

### 4. Evaluation
- **Metrics**: RMSE, R², MAE, MSE
- **Analysis**: Residual plots, feature importance
- **Segmentation**: By property type, region, price range
- **Statistical Testing**: Paired t-tests for significance

## Performance Optimization

### Spark Configuration
```yaml
Driver Memory: 8GB
Executor Memory: 8GB
Shuffle Partitions: 200
Adaptive Execution: Enabled
Serializer: KryoSerializer
```

### Optimization Strategies
- Broadcast joins for small dimension tables
- Persist() for reused DataFrames
- Partitioning by query patterns (year, property_type)
- Parquet columnar format for compression
- Adaptive query execution

### Scalability Analysis
- **Strong Scaling**: Fixed dataset, varying cores
- **Weak Scaling**: Dataset size scales with resources
- **Bottleneck Identification**: I/O vs compute analysis

## Data Schema

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | String | Unique sale ID |
| price | Integer | Sale price (£) |
| date_of_transfer | Date | Sale date |
| postcode | String | Property postcode |
| property_type | String | D=Detached, S=Semi, T=Terraced, F=Flat |
| old_new | String | Y=New build, N=Old |
| duration | String | F=Freehold, L=Leasehold |
| paon | String | House number/name |
| saon | String | Flat/apartment |
| street | String | Street name |
| locality | String | Local area |
| town_city | String | Town or city |
| district | String | Administrative district |
| county | String | County |
| ppd_category | String | A=Standard, B=Additional |
| record_status | String | A=Add, C=Change, D=Delete |

## Contributing

This is an academic project. For suggestions or improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request


