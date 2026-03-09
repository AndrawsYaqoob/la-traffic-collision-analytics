# LA Traffic Collision Analytics Platform

A data engineering and analytics project analyzing **600,000+ traffic collision records from Los Angeles County**.

This project demonstrates the design of a complete data pipeline including:

- relational database modeling
- ETL pipelines
- data warehouse architecture
- analytical dashboards
- enterprise reporting

The goal is to transform raw collision data into actionable insights about traffic safety patterns.

---

## Project Architecture

Raw Dataset (CSV)
        │
        ▼
ETL Pipeline 1 (SSIS)
        │
        ▼
Normalized Relational Database
        │
        ▼
ETL Pipeline 2 (SSIS)
        │
        ▼
Data Warehouse (Star Schema)
        │
        ▼
Analytics Layer
   ├─ Power BI Dashboards
   └─ SSRS Reports

Technologies used:

- Microsoft SQL Server
- SQL Server Integration Services (SSIS)
- Power BI
- SQL Server Reporting Services (SSRS)

---

## Dataset

This project uses **Traffic Collision Data from Los Angeles County**.

Source: Los Angeles Open Data Portal  
Dataset Link: https://data.lacity.org/Public-Safety/Traffic-Collision-Data-from-2010-to-Present/d5tf-ez2w/about_data

The dataset contains **600,000+ reported traffic collision incidents** recorded by the Los Angeles Police Department (LAPD).

Each record represents a single collision event and includes information about the time, location, and individuals involved.

### Key Attributes

The dataset includes several categories of attributes used for analysis:

**Incident Identification**
- `dr_no` – Division of Records Number (unique incident identifier)
- `crm_cd` – Crime code for the reported incident
- `crm_cd_desc` – Description of the crime code (Traffic Collision)

**Time Information**
- `date_rptd` – Date the incident was reported
- `date_occ` – Date the incident occurred
- `time_occ` – Time the incident occurred (24-hour format)

**Location Information**
- `area` – LAPD geographic area identifier (1–21)
- `area_name` – Name of the LAPD patrol division
- `rpt_dist_no` – Reporting district number
- `location` – Street address rounded to the nearest hundred block
- `cross_street` – Nearby intersection
- `location_1` – Geographic coordinates

**Victim Information**
- `vict_age` – Victim age
- `vict_sex` – Victim sex
- `vict_descent` – Victim descent code

**Incident Characteristics**
- `premis_cd` – Premise code describing the type of location
- `premis_desc` – Description of the premise
- `mocodes` – Modus Operandi codes describing incident characteristics

### Notes on Data Privacy

To protect privacy, exact addresses are not included in the dataset.  
Locations are rounded to the nearest 100 block and geographic coordinates represent approximate locations.

### Analytical Value

This dataset enables analysis of:

- collision frequency by time and date
- geographic hotspots for traffic incidents
- demographic characteristics of victims
- patterns related to location types and reporting districts

These insights can support traffic safety analysis and urban planning initiatives.

---

## Data Pipeline

### 1. Raw Data

The original dataset is provided in spreadsheet format.

Key characteristics:

- 600k+ records
- multiple categorical and numeric fields
- inconsistent formatting
- missing values in some columns

---

### 2. Staging Layer

Raw data is first loaded into staging tables using ETL.

Purpose:

- initial ingestion
- basic cleaning
- data type standardization

Tools used:

- SQL Server
- SSIS

---

### 3. Normalized Database Design

The staging data is transformed into a normalized relational schema.

Core tables include:

- Collisions
- Vehicles
- Victims
- Locations

This structure eliminates redundancy and improves data integrity.

---

### 4. Data Warehouse (Star Schema)

For analytics and reporting, a dimensional model is created.

Fact Table:

- Fact_Collisions

Dimension Tables:

- Dim_Date
- Dim_Location
- Dim_Vehicle
- Dim_Collision_Type

This schema enables efficient aggregation queries for analytics tools.

---

### 5. ETL Pipelines

ETL processes are implemented using **SQL Server Integration Services (SSIS)**.

Pipelines include:

- raw dataset ingestion
- transformation to normalized schema
- loading into the data warehouse

These processes automate the movement and transformation of data across layers.

---

## Analytics and Reporting

### Power BI Dashboard

Interactive dashboards built using **Power BI** provide visual insights into collision trends.

Key analyses include:

- collisions by year
- collisions by time of day
- high-risk intersections
- collision severity distribution
- geographic hotspots

---

### SSRS Reports

Formal analytical reports are generated using **SQL Server Reporting Services (SSRS)**.

Example report:

Traffic Collision Safety Report

Contents include:

- summary statistics
- top dangerous intersections
- fatality trends
- monthly collision patterns

These reports simulate enterprise reporting environments.

---

## Key Insights

Preliminary findings from the dataset include:

- Collision frequency peaks during evening commute hours.
- A small number of intersections account for a large share of incidents.
- Certain vehicle types have higher fatality rates in collisions.

Further analysis can support traffic safety planning and policy decisions.

---

## Repository Structure

la-traffic-collision-analytics

data/  
    dataset_source.md 
    sample_collision_dataset.xlsx
    descent_codes.xlsx
    mo_codes.xlsx
    sex_codes.xlsx

docs/  
    architecture_diagram.png  
    data_dictionary.md  

database/  
    normalized_schema.sql  
    indexes.sql  

warehouse/  
    star_schema.sql  

etl/  
    raw_to_normalized_etl.dtsx
    normalized_to_warehouse_etl.dtsx

powerbi/  
    collision_dashboard.pbix  

ssrs/  
    collision_report.rdl  

analysis/  
    collision_insights.md  

---

## How to Run the Project

// TO-BE ADDED

---

## Skills Demonstrated

This project demonstrates experience with:

- relational database design
- SQL query optimization
- ETL pipeline development
- dimensional data modeling
- data visualization
- enterprise reporting systems

---

## Data Attribution

This project uses publicly available data provided by the Los Angeles Open Data Portal.

The data is used for educational and analytical purposes only.