# Real Estate Market in Dubai

This project aims to analyze the real estate market in Dubai. The analysis involves scraping data from a property portal, cleaning and transforming the data, and then performing an analysis to derive meaningful insights. The following documentation provides a detailed overview of the steps and technologies used in this project.


![Project architecture](architecture.svg)


# Table of Contents

1. Problem Statement
2. Project Overview
3. Technologies Used
4. Data Collection
5. Data Pipeline
6. Data Analysis
7. Visualization
8. Conclusion

## Problem Statement

The primary objective of this project is to analyze the real estate market in Dubai. The steps involved in this project include:

- Collecting data from a property portal website.
- Cleaning and transforming the data.
- Analyzing the data.

## Project Overview

The project is divided into three main parts:

1. Collecting Data: Using the Scrapy Python library to scrape data from Bayut, a well-known property website in the UAE.

2. Data Pipeline: Creating a data pipeline using Google Cloud Platform (GCP) services to automate the data collection, cleaning, transformation, and analysis process.

3. Data Analysis: Using BigQuery for data analysis and Looker Studio for data visualization.

## Technologies Used

- Python: For scripting and data manipulation.
- Scrapy: For web scraping.
- Docker: To containerize the Scrapy project.
- Google Cloud Platform (GCP):
    - Artifact Registry
    - Cloud Run
    - Google Cloud Storage
    - DataProc
    - BigQuery
    - Cloud Composer
- Terraform: For infrastructure as code (IaC) to manage GCP services.
- Looker Studio: For data visualization.

## Data Collection

### Scraping Data

We used the Scrapy Python library to scrape data about the Dubai real estate market from Bayut. Scrapy is a powerful web scraping framework that allows for efficient data extraction from websites.

### Containerization with Docker

The Scrapy project is containerized using Docker to ensure consistency and ease of deployment. This allows the scraping job to be executed in an isolated environment, making it ready for the next steps in the data pipeline.

## Data Pipeline

### Overview
The data pipeline automates the process from data collection to visualization using various GCP services managed with Terraform.

### Steps
1. Docker Image Creation

    - Create a Docker image of the Scrapy project.
    - Push the Docker image to the Artifact Registry.

2. Data Collection with Cloud Run

    - Use Cloud Run to execute the Docker container.
    - After the scraping job is completed, save the data in a Google Cloud Storage bucket.

3. Data Processing with DataProc and PySpark

    - Use DataProc to run a PySpark job for cleaning and transforming the data.
    - Save the processed data back to the Google Cloud Storage bucket.

4. Data Analysis with BigQuery

    - Load the cleaned data into BigQuery.
    - Perform data analysis using SQL queries in BigQuery.

5. Data Visualization with Looker Studio

    - Use Looker Studio to create a report and visualize the analyzed data.

## Data Analysis

The data analysis step involves querying the cleaned data in BigQuery to derive insights into the Dubai real estate market. This includes analyzing trends, prices, property types, and other relevant metrics.

## Visualization

Looker Studio is used to create an interactive and informative report based on the analyzed data. This report provides a comprehensive view of the real estate market in Dubai, with various charts and graphs to highlight key findings.


## Conclusion

This project demonstrates the process of collecting, cleaning, transforming, and analyzing real estate data from Dubai using a combination of web scraping, cloud services, and data visualization tools.
The end-to-end pipeline ensures a streamlined and automated workflow, making it easier to derive actionable insights from the data.
