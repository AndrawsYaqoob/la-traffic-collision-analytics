import os
import sys
import pandas as pd
from datetime import datetime

# --- CONSTANTS ---

MO_VAL = "mo"
SEX_VAL = "sex"
DESCENT_VAL = "descent"
UNKNOWN_VAL = "X"

# Column names
COL_DR_NO          = "DR Number"
COL_DATE_REP       = "Date Reported"
COL_DATE_OCC       = "Date Occurred"
COL_TIME_OCC       = "Time Occurred"
COL_AREA_ID        = "Area ID"
COL_AREA_NAME      = "Area Name"
COL_RD             = "Reporting District"
COL_CRIME_CD       = "Crime Code"
COL_CRIME_DESC     = "Crime Code Description"
COL_MO_CODES       = "MO Codes"
COL_VIC_AGE        = "Victim Age"
COL_VIC_SEX        = "Victim Sex"
COL_VIC_DESCENT    = "Victim Descent"
COL_PREM_CD        = "Premise Code"
COL_PREM_DESC      = "Premise Description"
COL_ADDRESS        = "Address"
COL_CROSS_STREET   = "Cross Street"
COL_LOCATION       = "Location"

# New columns to be generated
COL_LATITUDE       = "Latitude"
COL_LONGITUDE      = "Longitude"

# Full list for the structural validation check
REQUIRED_COLUMNS = [
    COL_DR_NO, COL_DATE_REP, COL_DATE_OCC, COL_TIME_OCC,
    COL_AREA_ID, COL_AREA_NAME, COL_RD, COL_CRIME_CD, COL_CRIME_DESC,
    COL_MO_CODES, COL_VIC_AGE, COL_VIC_SEX, COL_VIC_DESCENT,
    COL_PREM_CD, COL_PREM_DESC, COL_ADDRESS, COL_CROSS_STREET, COL_LOCATION
]

# --- CONFIGURATION ---

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SOURCE_FILE = os.path.join(DATA_DIR, "sample_collision_dataset.xlsx")
CLEAN_OUTPUT = os.path.join(DATA_DIR, "cleaned_dataset.xlsx")
FAILED_OUTPUT = os.path.join(DATA_DIR, "failed_dataset.xlsx")

REF_FILES = {
    MO_VAL: os.path.join(DATA_DIR, "mo_codes.xlsx"),
    SEX_VAL: os.path.join(DATA_DIR, "sex_codes.xlsx"),
    DESCENT_VAL: os.path.join(DATA_DIR, "descent_codes.xlsx")
}

# --- 1. DATA ACQUISITION ---

def read_excel_file(path):
    """Reads an excel file and returns a DataFrame."""
    try:
        df = pd.read_excel(path)

        # A. PRE-REGISTER NEW COLUMNS
        # If we don't do this, Pandas won't 'see' the new columns added in row_level_logic
        df[COL_LATITUDE] = None
        df[COL_LONGITUDE] = None

        # Force date columns to string in the specific format mm/dd/yyyy
        # Errors='ignore' ensures that if a cell is already a string or null, it doesn't crash
        for col in [COL_DATE_REP, COL_DATE_OCC]:
            if col in df.columns:
                # Convert to datetime first (to handle any weird internal formats) 
                # then back to string in your desired input format
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%m/%d/%Y')

        return df
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        sys.exit(1)

def load_reference_sets(paths_dict):
    """Loads reference data into sets for O(1) lookup speed with MO code padding."""
    ref_data = {}
    for key, path in paths_dict.items():
        df = read_excel_file(path)
        
        # Get the first column as a Series
        col_data = df.iloc[:, 0].astype(str)
        
        if key == MO_VAL:
            # 1. Remove '.0' if Excel read it as a float
            # 2. Strip whitespace
            # 3. Pad with leading zeros to 4 digits
            cleaned_data = (col_data.str.replace(r'\.0$', '', regex=True)
                                    .str.strip()
                                    .str.zfill(4))
            ref_data[key] = set(cleaned_data.unique())
        else:
            # Standard lookup for Sex, Descent, etc.
            ref_data[key] = set(col_data.unique())
            
    return ref_data

# --- 2. ROW-LEVEL VALIDATION RULES ---

def validate_dr_number(value):
    """Check DR Number is not null and is only numbers."""
    val_str = str(value).strip()
    is_null = not val_str or val_str.lower() == 'none' or val_str.lower() == 'nan'
    if is_null:
        return None, "DR_Number is null"
    if not val_str.isdigit():
        return None, "DR_Number contains non-numeric characters"
    return val_str, None

def validate_and_reformat_date(value, col_name, required=True):
    """
    Validates mm/dd/yyyy. 
    - If null and required: adds error, skips parsing.
    - If null and not required: returns None (no error).
    - If present: attempts reformat to dd/mm/yyyy.
    """
    val_str = str(value).strip()
    is_null = not val_str or val_str.lower() == 'none' or val_str.lower() == 'nan'

    # 1. Handle Nulls
    if is_null:
        if required:
            return None, f"{col_name} is null but is required"
        return None, None  # Null is allowed, skip parsing

    # 2. Handle Parsing (Only if not null)
    try:
        dt_obj = datetime.strptime(val_str, '%m/%d/%Y')
        return dt_obj.strftime('%d/%m/%Y'), None
    except ValueError:
        return None, f"{col_name} is not in mm/dd/yyyy format"

def validate_and_reformat_time(value):
    """
    Check hhmm format.
    - Ensures 4 digits (pads if needed)
    - Validates HH (00-23) and MM (00-59)
    - Reformats to hh:mm:ss
    """
    val_str = str(value).strip()
    is_null = not val_str or val_str.lower() == 'none' or val_str.lower() == 'nan'
    
    # Clean up excel float artifacts (e.g., '1430.0' -> '1430')
    if '.' in val_str:
        val_str = val_str.split('.')[0]
        
    if is_null:
        return None, "Time_Occurred is null"
    
    # Pad to 4 digits (e.g., '830' -> '0830', '5' -> '0005')
    val_str = val_str.zfill(4)
    
    # Ensure it's numeric and length is correct
    if not val_str.isdigit() or len(val_str) != 4:
        return None, f"Time_Occurred '{val_str}' is not a valid 4-digit hhmm format"

    # Extract hours and minutes
    hours = int(val_str[:2])
    minutes = int(val_str[2:])

    # Check HH (0-23) and MM (0-59)
    if not (0 <= hours <= 23):
        return None, f"Time_Occurred '{val_str}' has invalid hours ({hours})"
    if not (0 <= minutes <= 59):
        return None, f"Time_Occurred '{val_str}' has invalid minutes ({minutes})"

    try:
        # Final safety parse and reformat
        dt_time = datetime.strptime(val_str, '%H%M')
        return dt_time.strftime('%H:%M:%S'), None
    except ValueError:
        return None, f"Time_Occurred '{val_str}' failed internal date conversion"

def validate_mo_codes(value, ref_data, mo_file_path):
    """
    Checks if MO codes exist. If a code is missing, adds it to the 
    reference Excel with name 'UNKNOWN'.
    """
    val_str = str(value).strip()
    is_null = not val_str or val_str.lower() == 'none' or val_str.lower() == 'nan'
    if is_null:
        return val_str, None  # Assuming MO Codes can be empty

    # MO codes are often space-separated strings in LAPD data
    codes = val_str.split()
    missing_codes = [c for c in codes if c not in ref_data[MO_VAL]]

    if missing_codes:
        # Load the actual file to append new rows
        mo_df = pd.read_excel(mo_file_path)
        
        for new_code in missing_codes:
            # Add to the set to prevent duplicate adds in the same run
            ref_data[MO_VAL].add(new_code)
            # Create new row
            new_row = pd.DataFrame([{"mo_code": new_code, "mo_name": "UNKNOWN"}])
            mo_df = pd.concat([mo_df, new_row], ignore_index=True)
        
        # Save the updated reference file back to disk
        mo_df.to_excel(mo_file_path, index=False)
        print(f"Updated {mo_file_path} with new codes: {missing_codes}")

    return val_str, None

def validate_victim_age(value):
    """Checks age is numeric, between 0-255, or null."""
    if pd.isna(value) or str(value).strip().lower() == 'none':
        return None, None # Valid as null
    
    try:
        age = int(float(value)) # Handle 25.0 cases
        if 0 <= age <= 255:
            return age, None
        else:
            return None, f"Victim_Age {age} out of bounds (0-255)"
    except ValueError:
        return None, f"Victim_Age '{value}' is not numeric"

def validate_with_reference(value, ref_set, col_name, unknown_value):
    """
    Checks if value exists in reference set. 
    If null or missing, returns the 'Unknown' value defined in the ref file.
    """
    val_str = str(value).strip()
    is_null = not val_str or val_str.lower() == 'none' or val_str.lower() == 'nan'
    
    # If null or empty, return the 'Unknown' marker (e.g., 'X')
    if is_null:
        return unknown_value, None
    
    # If value exists in the set, return it
    if val_str in ref_set:
        return val_str, None
    
    # If value is not null but not in reference, treat as invalid
    return None, f"{col_name} '{val_str}' not found in reference codes"

def parse_location(value):
    """
    Splits '(Latitude, Longitude)' string into separate float values.
    Example: '(34.063, -118.3141)' -> 34.063, -118.3141
    """
    val_str = str(value).strip()
    is_null = not val_str or val_str.lower() == 'none' or val_str.lower() == 'nan'

    if is_null or val_str == '(0, 0)':
        return None, None, None # Valid as nulls

    try:
        # Remove parentheses and split by comma
        clean_str = val_str.replace('(', '').replace(')', '')
        lat_str, lon_str = clean_str.split(',')
        
        return float(lat_str), float(lon_str), None
    except (ValueError, IndexError):
        return None, None, f"Location '{val_str}' is not in a valid (Lat, Long) format"

# --- 3. VALIDATION LOGIC ---

def validate_columns_exist(df, required_cols):
    """Ensures all required columns are present in the dataframe."""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        print(f"Validation Error: Missing columns {missing}")
        sys.exit(1)
    return True

def row_level_logic(row, ref_data):
    """
    Orchestrates the individual validation functions for each row.
    Updates the row in-place with cleaned/formatted data.
    """
    errors = []

    # 1. DR Number
    clean_dr, err = validate_dr_number(row.get(COL_DR_NO))
    if err: errors.append(err)
    else: row[COL_DR_NO] = clean_dr

    # 2. Date Reported
    clean_date_rep, err = validate_and_reformat_date(row.get(COL_DATE_REP), COL_DATE_REP, required=False)
    if err: errors.append(err)
    elif clean_date_rep: row[COL_DATE_REP] = clean_date_rep

    # 3. Date Occurred
    clean_date_occ, err = validate_and_reformat_date(row.get(COL_DATE_OCC), COL_DATE_OCC, required=True)
    if err: errors.append(err)
    elif clean_date_occ: row[COL_DATE_OCC] = clean_date_occ

    # 4. Time Occurred
    clean_time, err = validate_and_reformat_time(row.get(COL_TIME_OCC))
    if err: errors.append(err)
    else: row[COL_TIME_OCC] = clean_time

    # 5. MO Codes
    clean_mo, err = validate_mo_codes(row.get(COL_MO_CODES), ref_data, REF_FILES[MO_VAL])
    if err: errors.append(err)
    else: row[COL_MO_CODES] = clean_mo

    # 6. Victim Age
    clean_age, err = validate_victim_age(row.get(COL_VIC_AGE))
    if err: errors.append(err)
    else: row[COL_VIC_AGE] = clean_age

    # 7. Victim Sex
    clean_sex, err = validate_with_reference(
        row.get(COL_VIC_SEX), 
        ref_data[SEX_VAL], 
        COL_VIC_SEX, 
        UNKNOWN_VAL
    )
    if err: errors.append(err)
    else: row[COL_VIC_SEX] = clean_sex

    # 8. Victim Descent
    clean_descent, err = validate_with_reference(
        row.get(COL_VIC_DESCENT), 
        ref_data[DESCENT_VAL], 
        COL_VIC_DESCENT, 
        UNKNOWN_VAL
    )
    if err: errors.append(err)
    else: row[COL_VIC_DESCENT] = clean_descent

    # 9. Location
    lat, lon, err = parse_location(row.get(COL_LOCATION))
    if err:
        errors.append(err)
    else:
        # Create new columns in the row dictionary
        row[COL_LATITUDE] = lat
        row[COL_LONGITUDE] = lon

    return "; ".join(errors) if errors else None

def segregate_data(df, ref_data):
    # This list will hold our updated rows
    processed_rows = []
    failed_rows = []

    for index, row in df.iterrows():
        # row_level_logic updates the 'row' object in-place
        error_msg = row_level_logic(row, ref_data)
        
        if error_msg:
            # We add the reason to a copy of the row for the failed file
            failed_row = row.copy()
            failed_row['Failure_Reason'] = error_msg
            failed_rows.append(failed_row)
        else:
            # This row now contains the new Lat/Long and cleaned dates
            processed_rows.append(row)

    # Rebuild DataFrames from the lists of Series
    clean_df = pd.DataFrame(processed_rows)
    failed_df = pd.DataFrame(failed_rows)
    
    return clean_df, failed_df

# --- 4. OUTPUT ---

def export_to_excel(df, output_path, sheet_name="Data"):
    """Writes a dataframe to an excel file."""
    try:
        df.to_excel(output_path, index=False, sheet_name=sheet_name)
        print(f"Successfully exported: {output_path}")
    except Exception as e:
        print(f"Error exporting to {output_path}: {e}")

# --- 5. MAIN ORCHESTRATION ---

def main():
    # 1. Load Data
    raw_data = read_excel_file(SOURCE_FILE)
    reference_data = load_reference_sets(REF_FILES)
    
    # 2. Validate Structure
    validate_columns_exist(raw_data, REQUIRED_COLUMNS)
    
    # 3. Validate Content & Segregate
    clean_df, failed_df = segregate_data(raw_data, reference_data)
    
    # 4. Output Results
    export_to_excel(clean_df, CLEAN_OUTPUT, "Data")
    export_to_excel(failed_df, FAILED_OUTPUT, "Failed_Rows")

    print(f"Process Complete. Clean: {len(clean_df)} | Failed: {len(failed_df)}")

if __name__ == "__main__":
    main()