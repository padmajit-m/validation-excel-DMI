import streamlit as st
import pandas as pd
import re

# Load your mapping file from JSON or other formats
# This is a simplified example based on your provided mapping structure.
mapping = {
    # Example mapping - you should load this from your file
    "householdRentExpense": {
        "type": "string",
        "flatFileHeader": "Household Rent Expense",
        "pattern": "^\d+(\.\d+)?$",
        "customValidator": ["PATTERN_VALIDATION"],
        "required": "true",
        "fieldType": "direct"
    },
    # Add other mappings
    # Ensure this is populated with your full 1000+ row mapping
}

def validate_header(headers):
    expected_headers = {details["flatFileHeader"] for details in mapping.values() if "flatFileHeader" in details}
    missing_headers = expected_headers - set(headers)
    extra_headers = set(headers) - expected_headers
    return missing_headers, extra_headers

def validate_data(df):
    issues = []
    for col, details in mapping.items():
        flat_file_header = details.get("flatFileHeader")
        if flat_file_header:
            if flat_file_header not in df.columns:
                issues.append(f"Missing column '{flat_file_header}'")
                continue
            
            pattern = details.get("pattern")
            if pattern:
                regex = re.compile(pattern)
                invalid_data = df[flat_file_header].apply(lambda x: not regex.match(str(x)))
                if invalid_data.any():
                    invalid_rows = df[invalid_data].index.tolist()
                    issues.append(f"Invalid data in column '{flat_file_header}' at rows: {', '.join(map(str, invalid_rows))}")
            
            # Check for required fields
            if details.get("required") == "true":
                missing_data = df[flat_file_header].isnull() | (df[flat_file_header] == '')
                if missing_data.any():
                    missing_rows = df[missing_data].index.tolist()
                    issues.append(f"Missing required data in column '{flat_file_header}' at rows: {', '.join(map(str, missing_rows))}")
    return issues

def main():
    st.title("Excel Validation App")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            headers = df.columns.tolist()
            
            # Validate headers
            missing_headers, extra_headers = validate_header(headers)
            if missing_headers:
                st.error(f"Missing headers: {', '.join(missing_headers)}")
            if extra_headers:
                st.error(f"Extra headers: {', '.join(extra_headers)}")
            
            # Validate data
            data_issues = validate_data(df)
            if data_issues:
                for issue in data_issues:
                    st.error(issue)
            else:
                st.success("The Excel file is valid!")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
