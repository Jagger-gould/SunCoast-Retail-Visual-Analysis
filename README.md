# SunCoast-Retail-Visual-Analysis
In this project, you’ll see how data is brought to life using visualizations that highlight patterns, trends, and insights. We’ll use Matplotlib, a foundational Python library, to create common business charts, such as bar graphs, line charts, and scatter plots.  

This project uses **Python**, **Pandas**, **NumPy**, and **Matplotlib** to generate and visualize retail data for a fictional company called **SunCoast Retail**. The goal is to create meaningful visual insights from structured datasets using different types of charts.

## Project Overview

The code simulates both **sales data** and **customer data**, then uses multiple visualization techniques to analyze trends, performance, and relationships across the business.

## What the Code Does

### 1. Data Generation
- Creates quarterly sales data for:
  - 4 locations (Tampa, Miami, Orlando, Jacksonville)
  - 5 product categories
- Includes factors like:
  - Seasonal trends
  - Location performance
  - Category performance
  - Business growth over time
- Generates customer data including:
  - Age
  - Purchase amount
  - Preferred category
  - Price tier

### 2. Data Preparation
- Converts generated data into Pandas DataFrames
- Adds helpful columns like:
  - Quarter number
  - Sales per advertising dollar

## Visualizations Created

The project builds a wide range of charts:

### Time-Based Charts
- Line chart of total quarterly sales
- Multi-line chart comparing sales by location

### Category & Location Analysis
- Grouped bar chart for category performance by location
- Stacked bar chart for sales composition by location

### Advertising Insights
- Scatter plot of ad spend vs sales (with trendline)
- Line chart of advertising efficiency over time

### Customer Insights
- Histograms of customer age distribution (overall + by location)
- Box plot of purchase amount by age group
- Histogram of purchase amounts

### Market Share & Distribution
- Pie chart for sales by price tier
- Pie chart for category market share
- Pie chart for sales by location

### Dashboard
- A combined 4-panel dashboard showing:
  - Sales trends
  - Sales by location
  - Ad spend vs sales
  - Category market share

## Key Insights

- Sales show steady growth with strong Q4 seasonal spikes
- Miami is the top-performing location
- Electronics generate the highest revenue
- Higher ad spend is associated with higher sales
- Customer demographics vary by location
- Mid-range and premium products drive significant revenue

## How to Run

1. Install required libraries:
   ```bash
   pip install pandas numpy matplotlib
