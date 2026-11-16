
# Sales Analytics Platform

## Overview

Interactive business intelligence platform designed
to analyze sales performance and extract actionable
business insights.

Built using Python, Pandas, NumPy, SQLite,
Plotly and Streamlit.

## Objectives

- Clean and transform raw sales data.
- Identify missing and duplicate records.
- Store processed data in SQLite.
- Calculate business KPIs.
- Analyze revenue and profit.
- Compare products, categories and regions.
- Generate interactive visualizations.
- Export filtered sales reports.

## Technologies

- Python 3.12
- Pandas
- NumPy
- Matplotlib
- Plotly
- SQLite
- SQL
- Streamlit
- Pytest
- Git / GitHub

## Architecture

Raw CSV
   |
   v
Data Cleaning (Pandas)
   |
   v
Data Transformation
   |
   v
SQLite Database
   |
   v
Streamlit Dashboard

## Project Structure

Sales-Analytics-Platform/
    data/
        raw/
        processed/
    database/
        sales.db
    src/
        cleaning.py
        database.py
    tests/
        test_cleaning.py
    sql/
        analysis_queries.sql
    generate_data.py
    prepare_data.py
    app.py
    requirements.txt
    README.md

## Installation

Clone repository:

git clone YOUR_REPOSITORY_URL

Enter project:

cd Sales-Analytics-Platform

Create virtual environment:

python -m venv .venv

Activate environment:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Generate Dataset

python generate_data.py

## Prepare Data

python prepare_data.py

## Run Tests

pytest -v

## Launch Dashboard

python -m streamlit run app.py

## Dashboard Features

- Revenue and profit KPIs
- Monthly sales analysis
- Product performance
- Category analysis
- Regional analysis
- Payment method distribution
- Interactive filtering
- CSV export

## Data Disclaimer

This project uses fictional, synthetically
generated sales data. It does not represent
real customers or commercial transactions.

## Future Improvements

- PostgreSQL integration
- Automated ETL scheduling
- Cloud deployment
- Authentication
- Advanced sales forecasting
- Docker containerization

## Author

Chebbi Dhia
