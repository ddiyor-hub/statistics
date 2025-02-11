# 📊 Statistics Web App

A Streamlit-based web application for comprehensive statistical analysis of numerical datasets. Visualize distributions, relationships, and key statistics through interactive plots and tables.

![App Screenshot](https://via.placeholder.com/800x400.png?text=Statistics+Web+App+Screenshot)

## Features

- **📁 File Upload**: Supports CSV files with automatic numeric column detection
- **🔍 Data Overview**: 
  - Interactive dataset preview
  - Column type summary
  - Basic dataset statistics
- **📈 Visualization Tools**:
  - Scatter plots with customizable axes
  - Box plots for outlier detection
  - Distribution histograms
  - Skewness analysis bar charts
- **📊 Statistical Analysis**:
  - Descriptive statistics (mean, median, quantiles)
  - Skewness and kurtosis values
  - Interactive correlation exploration
- **📥 Export Capabilities**:
  - Download statistical summaries as CSV
  - Save visualizations as PNG

## Installation

### Using Conda

1. Create environment:
```bash
conda create -n stats_app python=3.11  ( !if you dont have conda you can just use pip with python 3.11)

2. Activate environment:
conda activate stats_app

3. Install dependencies:
conda install streamlit pandas numpy matplotlib


### Usage

Launch the app:

streamlit run main.py