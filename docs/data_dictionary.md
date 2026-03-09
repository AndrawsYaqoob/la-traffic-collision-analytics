# Data Dictionary

This document provides detailed information about the **LA County Sheriff Traffic Collision Database and Warehouse**.  
It includes all tables, columns, data types, and descriptions for the normalized database.

---

## Database: SheriffIncidents

### Dimension Tables

#### **dim_area**

| Column | Type | Description |
|--------|------|-------------|
| area_id | INT | Unique identifier for each LAPD geographic area (1–21) |
| area_name | VARCHAR(200) | Name of the patrol division corresponding to the area (e.g., "77th Street Division") |

---

#### **dim_crime**

| Column | Type | Description |
|--------|------|-------------|
| crime_code | INT | Unique code representing a type of incident (all 997 for traffic collisions in this dataset) |
| crime_name | VARCHAR(200) | Description of the crime code (e.g., "Traffic Collision") |

---

#### **dim_mo**

| Column | Type | Description |
|--------|------|-------------|
| mo_code | INT | Unique Modus Operandi code |
| mo_name | VARCHAR(500) | Description of the MO code; used in bridge table for multi-valued MO per report |

---

#### **dim_descent**

| Column | Type | Description |
|--------|------|-------------|
| descent_code | CHAR(1) | Code representing victim descent/ethnicity |
| descent_name | VARCHAR(200) | Full name corresponding to the descent code (e.g., "H - Hispanic/Latin/Mexican") |

---

#### **dim_sex**

| Column | Type | Description |
|--------|------|-------------|
| sex_code | CHAR(1) | Code representing victim sex (F, M, X) |
| sex_name | VARCHAR(200) | Full description of the sex code (e.g., "F - Female") |

---

#### **dim_premise**

| Column | Type | Description |
|--------|------|-------------|
| premise_code | INT | Code representing type of location where collision occurred |
| premise_name | VARCHAR(200) | Description of premise type (e.g., "Street", "Parking Lot") |

---

### Fact Table

#### **fact_report**

| Column | Type | Description |
|--------|------|-------------|
| report_number | BIGINT | Unique identifier for each collision report |
| date_reported | DATE | Date the collision was reported |
| date_occurred | DATE | Date the collision actually occurred |
| time_occurred | TIME | Time the collision occurred |
| area_id | INT | Foreign key to `dim_area` (location of collision) |
| crime_code | INT | Foreign key to `dim_crime` |
| victim_age | TINYINT | Age of the victim |
| victim_sex | CHAR(1) | Foreign key to `dim_sex` |
| victim_descent | CHAR(1) | Foreign key to `dim_descent` |
| premise_code | INT | Foreign key to `dim_premise` |
| address | VARCHAR(500) | Rounded street address of incident |
| cross_street | VARCHAR(500) | Cross street of incident location |
| latitude | DECIMAL(9,6) | Latitude of incident (rounded) |
| longitude | DECIMAL(9,6) | Longitude of incident (rounded) |

**Constraints / Relationships:**

- `area_id` → `dim_area(area_id)`  
- `crime_code` → `dim_crime(crime_code)`  
- `victim_sex` → `dim_sex(sex_code)`  
- `victim_descent` → `dim_descent(descent_code)`  
- `premise_code` → `dim_premise(premise_code)`

---

### Bridge Table

#### **bridge_report_mo_code**

| Column | Type | Description |
|--------|------|-------------|
| report_number | BIGINT | Foreign key to `fact_report(report_number)` |
| mo_code | INT | Foreign key to `dim_mo(mo_code)`; represents a single MO code per report |

**Notes:**  

- Composite primary key: `(report_number, mo_code)`  
- Handles **many-to-many relationship** between collision reports and MO codes.

---

### Staging Table

#### **stg_mo_raw**

| Column | Type | Description |
|--------|------|-------------|
| report_number | BIGINT | Corresponding report identifier from `fact_report` |
| mo_codes_raw | VARCHAR(1000) | Raw space-separated MO codes (e.g., "3004 3027 3034") used as input to populate `bridge_report_mo_code` via ETL |

**Notes:**  

- This table is used **only during ETL** to transform multi-valued MO codes into a normalized bridge table.  
- After ETL, this table can be archived or truncated.

---
