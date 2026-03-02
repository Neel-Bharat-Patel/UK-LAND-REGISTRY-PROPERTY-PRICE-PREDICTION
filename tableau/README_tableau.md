# Tableau Dashboards - UK Property Price Prediction

This directory contains Tableau dashboard specifications and data exports for visualization.

## Dashboard Overview

### Dashboard 1: Data Quality & Pipeline Monitoring
**Purpose**: Monitor data ingestion quality and processing pipeline performance

**Sheets**:
1. **Data Volume by Year**
   - Visualization: Bar chart
   - Metrics: Transaction count, total value
   - Filters: Year, property type
   - Insight: Data distribution across years

2. **Missing Values Heatmap**
   - Visualization: Heatmap
   - Metrics: Null percentage by column
   - Filters: Dataset version
   - Insight: Data completeness assessment

**Data Sources**:
- `property_prices.parquet` (sampled)
- `data_quality_metrics.csv`

---

### Dashboard 2: Model Performance & Feature Importance
**Purpose**: Compare ML model performance and understand feature contributions

**Sheets**:
1. **Model Comparison Metrics**
   - Visualization: Grouped bar chart
   - Metrics: RMSE, R², MAE
   - Comparison: 5 models side-by-side
   - Insight: Best performing model identification

2. **Feature Importance Chart**
   - Visualization: Horizontal bar chart
   - Metrics: Feature importance scores
   - Top features: Top 15 displayed
   - Insight: Key price prediction drivers

**Data Sources**:
- `model_performance.csv`
- `feature_importance.csv`
- `final_model_results.csv`

---

### Dashboard 3: Business Insights & Predictions
**Purpose**: Provide actionable business insights and regional analysis

**Sheets**:
1. **Price Predictions by Region**
   - Visualization: Geographic map + scatter plot
   - Metrics: Avg predicted price, prediction error
   - Filters: Region, property type, year
   - Insight: Regional price patterns

2. **Performance by Property Type**
   - Visualization: Box plot + summary table
   - Metrics: RMSE by type, transaction count
   - Breakdown: D, S, T, F categories
   - Insight: Model accuracy by segment

**Data Sources**:
- `detailed_predictions.csv`
- `performance_by_property_type.csv`
- `performance_by_region.csv`
- `performance_by_price_range.csv`

---

### Dashboard 4: Scalability & Cost Analysis
**Purpose**: Analyze distributed computing performance and resource efficiency

**Sheets**:
1. **Training Time vs Data Size**
   - Visualization: Line chart with trend
   - Metrics: Training time, data size
   - Analysis: Scaling efficiency
   - Insight: Resource requirements prediction

2. **Resource Utilization**
   - Visualization: Dual-axis chart
   - Metrics: Memory usage, CPU %, execution time
   - Breakdown: By pipeline stage
   - Insight: Bottleneck identification

**Data Sources**:
- `scalability_data.csv`
- `performance_metrics.csv`
- `pipeline_results.csv`

---

## Data Files

### Generated CSV Files

| File | Description | Rows | Columns |
|------|-------------|------|---------|
| `model_performance.csv` | ML model comparison metrics | 5 | 5 |
| `feature_importance.csv` | Feature importance scores | ~50 | 2 |
| `detailed_predictions.csv` | Sample predictions with errors | ~67,000 | 7 |
| `performance_by_property_type.csv` | Metrics by property type | 4 | 6 |
| `performance_by_region.csv` | Top 20 regions by error | 20 | 3 |
| `performance_by_price_range.csv` | Metrics by price bracket | 5 | 3 |
| `scalability_data.csv` | Training time vs data size | 4 | 3 |
| `evaluation_summary.csv` | Overall project summary | 1 | 7 |

---

## Tableau Public Workbook

### Publishing Instructions

1. **Open Tableau Desktop/Public**

2. **Connect to Data Sources**
   - File → Open → Navigate to `tableau/` folder
   - Connect to each CSV file
   - Create data extracts for performance

3. **Create Dashboard 1**
   - Create new sheet "Data Volume by Year"
   - Drag year to columns, count to rows
   - Add property_type to color
   - Create new sheet "Missing Values Heatmap"
   - Use calculated field for null percentages
   - Combine into Dashboard 1

4. **Create Dashboard 2**
   - Create "Model Comparison Metrics" sheet
   - Use model_performance.csv
   - Create grouped bar chart (Model × Metric)
   - Create "Feature Importance Chart"
   - Use feature_importance.csv
   - Sort by importance descending
   - Combine into Dashboard 2

5. **Create Dashboard 3**
   - Create "Price Predictions by Region"
   - Use detailed_predictions.csv
   - Create map using postcode_area
   - Add prediction error as color
   - Create "Performance by Property Type"
   - Use performance_by_property_type.csv
   - Create box plot showing error distribution
   - Combine into Dashboard 3

6. **Create Dashboard 4**
   - Create "Training Time vs Data Size"
   - Use scalability_data.csv
   - Line chart with trend line
   - Create "Resource Utilization"
   - Use performance_metrics.csv
   - Dual-axis chart (Memory + CPU)
   - Combine into Dashboard 4

7. **Publish to Tableau Public**
   - Server → Tableau Public → Save to Tableau Public
   - Name: "UK Property Price Prediction Analysis"
   - Get shareable link

---

## Dashboard Design Principles

### Visual Design
- **Color Palette**: Tableau 10 (consistent across dashboards)
- **Font**: Arial, 11pt body, 14pt headers
- **Layout**: Mobile-responsive grid
- **Interactivity**: Cross-dashboard filtering enabled

### Performance Optimization
- **Extracts**: All data sources use extracts
- **Aggregation**: Pre-aggregated where possible
- **LOD Calculations**: Efficient level-of-detail expressions
- **Sampling**: Large datasets sampled (1% for predictions)

### Best Practices
- Clear titles and descriptions
- Legends positioned consistently
- Tooltips with detailed information
- Action filters between sheets
- Export-friendly layouts

---

## Interactive Features

### Parameters
- `Year_Filter`: Select analysis year
- `Property_Type_Filter`: Filter by D/S/T/F
- `Region_Filter`: Select postcode area
- `Price_Range`: Filter by price bracket

### Actions
- **Highlight**: Hover to highlight related data
- **Filter**: Click to filter other sheets
- **URL**: Link to detailed reports
- **Set**: Create custom groups

### Calculated Fields

```
// Prediction Error Percentage
ABS([Actual Price] - [Predicted Price]) / [Actual Price] * 100

// Error Category
IF [Absolute Error] < 50000 THEN "Low"
ELSEIF [Absolute Error] < 100000 THEN "Medium"
ELSE "High"
END

// Price Per SqFt (if area data available)
[Price] / [Area]
```

---

## Sharing & Export

### Tableau Public Link
**URL**: [To be added after publishing]

### Export Options
- **PDF**: File → Export as PDF
- **Image**: Dashboard → Export Image
- **PowerPoint**: File → Export as PowerPoint
- **Data**: Download → Crosstab to Excel

### Embed Code
```html
<div class='tableauPlaceholder'>
  <object class='tableauViz' width='100%' height='850px'>
    <param name='host_url' value='https://public.tableau.com/' />
    <param name='embed_code_version' value='3' />
    <param name='site_root' value='' />
    <param name='name' value='[workbook-name]' />
  </object>
</div>
```

---

## Troubleshooting

### Common Issues

**Issue**: Data not loading
- **Solution**: Check file paths, ensure CSV files exist

**Issue**: Slow dashboard performance
- **Solution**: Reduce data size, use extracts, optimize calculations

**Issue**: Maps not displaying
- **Solution**: Ensure postcode format is correct, use geographic roles

**Issue**: Filters not working
- **Solution**: Check action filters, verify field relationships

---

## Maintenance

### Data Refresh Schedule
- **Frequency**: After each model training run
- **Process**: 
  1. Run all notebooks
  2. Export CSVs to tableau/
  3. Refresh Tableau extracts
  4. Republish to Tableau Public

### Version Control
- Dashboard versions saved as .twbx files
- Naming: `dashboard[N]_v[X.Y].twbx`
- Keep archive of previous versions

---

## Contact & Support

For dashboard-related questions:
- Check Tableau Public community forums
- Review Tableau documentation
- Submit issues via project repository

---

**Last Updated**: February 26, 2026
**Tableau Version**: 2023.3+
**Status**: Ready for creation
