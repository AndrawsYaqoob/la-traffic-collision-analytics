# Dataset Source

## Dataset Information

**Name:** Traffic Collision Data  
**Source:** Los Angeles Open Data Portal  
**Link:** [https://data.lacity.org/Public-Safety/Traffic-Collision-Data-from-2010-to-Present/d5tf-ez2w/about_data](https://data.lacity.org/Public-Safety/Traffic-Collision-Data-from-2010-to-Present/d5tf-ez2w/about_data)  
**Records:** ~600,000 reported traffic collision incidents  
**Coverage:** Los Angeles County  
**Collected by:** Los Angeles Police Department (LAPD)

This dataset contains detailed information on traffic collisions, including dates, times, locations, involved individuals, and incident characteristics. It is used for analysis of collision trends, geographic hotspots, and victim demographics.

---

## Key Fields

| Category | Column | Description |
|----------|--------|-------------|
| Incident ID | `dr_no` | Unique Division of Records Number for the incident |
| Time | `date_rptd`, `date_occ`, `time_occ` | Date reported, date occurred, and time of collision |
| Location | `area`, `area_name`, `rpt_dist_no`, `location`, `cross_street`, `location_1` | LAPD area ID and name, reporting district, rounded street address, cross street, and approximate coordinates |
| Victim | `vict_age`, `vict_sex`, `vict_descent` | Age, sex, and descent/ethnicity of the victim |
| Incident Type | `crm_cd`, `crm_cd_desc`, `mocodes` | Crime code (997 = traffic collision), description, and Modus Operandi codes |
| Premise | `premis_cd`, `premis_desc` | Type of location where collision occurred and its description |

---

## Reference / Lookup Files

The following Excel files are included in the repository to support populating the normalized database:

| File Name | Purpose |
|-----------|---------|
| `descent_codes.xlsx` | Maps victim descent codes (A–Z) to full ethnicity descriptions. Used to populate the `VictimDescent` dimension table. |
| `mo_codes.xlsx` | Lists Modus Operandi codes and descriptions. Used to populate the `ModusOperandi` table in the normalized database. |
| `sex_codes.xlsx` | Maps sex codes (F, M, X) to full descriptions. Used to populate the `VictimSex` table in the normalized database. |

These files are **small, structured datasets** used to ensure data consistency when transforming raw collision records into a normalized relational schema. They are referenced during ETL to replace coded values with descriptive attributes.

--

## Common Data Formatting Issues

Some fields in the raw dataset required preprocessing before loading into SQL Server:

- **Date Occurred / Date Reported:** Original format `MM/DD/YYYY`; needed conversion to `YYYY-MM-DD` for SQL compatibility.  
- **Time Occurred:** Original format `HHMM` (e.g., 2345); converted to `HH:MM:SS` for SQL datetime types.  
- **Location:** Original format `(latitude, longitude)`; split into separate `Latitude` and `Longitude` fields to store as numeric columns.

--

## Notes

- **Privacy:** Exact addresses are rounded to the nearest 100 block to protect privacy. Geographic coordinates are approximate.  
- **Use:** This dataset is intended for educational and analytical purposes only.  
