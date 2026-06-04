# DCM (Data Catalog for Motorization)

A comprehensive analytical dashboard and data processing pipeline for vehicle registration data in Poland. DCM processes, cleans, and visualizes over two decades of passenger car registrations based on the Central Register of Vehicles and Drivers (CEPiK) data.

> **Status:** Project finished.

## Overview

DCM is built to handle large-scale historical datasets (covering the period from 01.01.2000 to 20.05.2026). It provides a high-level statistical overview of the Polish automotive market, tracking fleet evolution, regional distribution, and the ongoing shift in fuel types (EV/hybrid penetration).

## Core Features

* **Batch & Incremental Data Loading:** The system handles a primary historical batch of all Polish voivodeships (filtered strictly to passenger cars in the `only_cars` table). It utilizes delta logic to fetch and load only new registrations, avoiding full database rebuilds.
* **Data Quality Pipeline:** Built-in mechanisms to handle raw, dirty records. The pipeline actively corrects misspelled brand names, standardizes missing values, and drops or flags invalid registration dates (e.g., year 3000 anomalies).
* **Historical Snapshots:** Tools to compare the state of the fleet across different timeframes (e.g., YoY brand market share).
* **Regional Granularity:** Data aggregation goes beyond standard voivodeship levels, allowing for deep-dive statistical breakdowns by *powiat* (county).
* **Fuel Trend Analysis:** Dedicated analytics for tracking the transition from combustion engines to alternative fuel sources over time.
* **Streamlit Frontend:** A lightweight, interactive web interface for data exploration and visualization.

## Architecture Notes & API Constraints

During the development of DCM, the initial architecture assumed daily automated data fetching via the public CEPIK API. However, due to severe endpoint instability, connection timeouts, and poor data quality in the daily delta feeds, this approach was deprecated. 

The current architecture relies on stable historical data dumps and controlled incremental loading, ensuring data integrity and application reliability. External data enrichment (e.g., GUS demographics, fuel prices) has also been scoped out to maintain focus on the core registry analytics.

## Installation & Setup

To run the dashboard locally:

1. Clone the repository:
   ```bash
   git clone [https://github.com/justgodtears/DCM.git](https://github.com/justgodtears/DCM.git)
   cd DCM
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
3. Configure your database connection in .streamlit/secrets.toml (refer to the documentation for schema requirements).
4. Run the Streamlit application:
   ```bash
   streamlit run app.py

## License

Created by [@justgodtears](https://github.com/justgodtears).
