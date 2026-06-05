**MTA Congestion Relief Analytics Dashboard**
This project provides a data-driven visualization platform for analyzing traffic patterns within the New York Congestion Relief Zone (CRZ). It automates the collection, summarization, and visualization of MTA mobility data to help urban planners and policy analysts benchmark hourly traffic trends against historical averages.

**Live Dashboard**
View the live visualization here:
**__https://hoffmanap.github.io/congestionpricing/__**

**Features**
**Automated Data Pipeline**: Uses GitHub Actions to daily fetch raw mobility data from the NY Data Portal.

**Server-Side Aggregation**: A Python-based summarization engine reduces 50,000+ raw records into a lightweight summary.json file, ensuring the dashboard loads instantly.

**Comparative Benchmarking**: Automatically identifies the most recent data day and plots it against historical daily averages to visualize current performance trends.

**Geo-Spatial Splicing**: Filter data by specific detection_region (e.g., Lincoln Tunnel, Queensboro Bridge) to compare mobility trends across the zone.

**Tech Stack**
Data Source: MTA Congestion Relief Data (Socrata API).

Automation: GitHub Actions (scheduled daily at midnight UTC).

Data Processing: Python (pandas) for heavy-duty aggregation.

Visualization: Chart.js for dynamic, browser-based temporal analysis.

Styling: Tailwind CSS.

**Project Structure**
.github/workflows/fetch-data.yml: Automates the daily data ingestion and summarization.

summarize.py: The Python script that aggregates hourly data and calculates metrics.

index.html: The frontend dashboard with interactive filters and charting logic.

summary.json: The generated, lightweight data file powering the dashboard.

**Deployment & Development**
This project is hosted on GitHub Pages. Any updates to the code in the main branch are automatically deployed. To modify the dashboard, ensure you have the API_KEY (App Token) stored in your repository's Secrets and variables under Settings > Actions.
