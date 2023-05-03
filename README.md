
# ETL Pipeline Postgres & Airflow


# Introduction
The goal of this project is to build a data processing pipeline that extracts information about new users every minute from an API, transforms the data and stores it in a Postgres database.

# Objectives of this project
- Understand how to use python libraries (Psycopg2) to interact with databases;
- Understand how to use JSON schema validation in order to perform data quality checks;
- Build an Airflow DAG and understand how to orchestrate a batch processing pipeline and connect to external sources;
- Setup a docker container that contains all dependencies needed for the project (Airflow webserver, scheduler, worker, Postgres DB etc);
- Understand how to use unittesting python libraries (Unittest) to perform automated testing;

# Contents
- [The Data Set](#the-data-set)
- [Used Tools](#used-tools)
  - [Client](#client)
  - [Storage](#storage)
  - [Orchestration](#orchestration)
- [Pipelines](#pipelines)
  - [Batch Processing](#batch-processing)
- [Demo](#demo)
- [Conclusion](#conclusion)
- [Appendix](#appendix)


# The Data Set
The data used in this project is pulled from the following API: https://randomuser.me/. This is a free, open-source API for generating random user data.

# Used Tools
![Diagram - tools](https://user-images.githubusercontent.com/108272657/235611932-d72c0476-c39d-4196-8a6b-58e61102d107.svg)


## Client
The source data for the batch processing pipeline is located in the on a GitHub repo in .csv format. The .csv data will be read by the local python script.
## Storage
S3: Amazon Simple Storage Service is a service that acts as a data lake in this project. Source sales transactions are hosted here for batch/bulk load.
Redshift: Datawareouse or OLAP database. A star schema has been built for this project on this relational database.
## Orchestration
Apache Airflow is used to orchestrate this data pipeline.
## Visualization
Grafana: Dasboards are built to visualize the data from the Redshift data warehouse and S3.

# Pipelines
## Batch Processing
S3 Data Lake: Here are the sales transactions that are dumped in the .csv format.

Amazon Redshift: Redshift is Amazon's analytics database, and is designed to crunch large amounts of data as a data warehouse. A redshift cluster has been created for this project as a OLAP Database. Once the database has been created, a staging table has been created. Then the redshift copy command has been used to copy the .csv data from S3 to the created table. Then the star schema tables has been created in the data warehouse and loaded by the data warehouse procedure. Changes in products and customers dimensions are tracked using SCD type 2.

--- Orchestration to be completed ---

## Visualizations
-- To be completed --

# Demo
-- To be completed --

# Conclusion
Through the completion of this data engineering project, I have gained experience in the utilization of fundamental AWS services, including S3 and Redshift. This hands-on experience has enabled me to develop a deeper understanding of the AWS infrastructure and its capabilities for processing large-scale datasets. As a result of this project, I have gained the confidence and competence to effectively execute future data engineering projects within the AWS ecosystem.
