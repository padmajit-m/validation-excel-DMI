import streamlit as st
import pandas as pd
import re
from openpyxl import load_workbook

# Check for openpyxl
try:
    import openpyxl
except ImportError:
    st.error("openpyxl is not installed.")
    st.stop()

def validate_excel(file, mapping):
    # Load Excel file
    try:
        df = pd.read_excel(file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return

    errors = []

    # Validate headers
    for header in df.columns:
        if header not in mapping:
            errors.append(f"Invalid header: {header}")

    # Additional validation logic based on the mapping file
    for index, row in df.iterrows():
        for key, value in mapping.items():
            if key in row:
                # Validate based on type and pattern
                if value.get('type') == 'string':
                    pattern = value.get('pattern')
                    if pattern and not re.match(pattern, str(row[key])):
                        errors.append(f"Invalid value in field '{key}': {row[key]}")

    if errors:
        st.error("Validation errors found:")
        for error in errors:
            st.write(error)
    else:
        st.success("Validation passed.")

# Streamlit UI
st.title('Excel Validation Tool')
uploaded_file = st.file_uploader("Upload your Excel file", type="xlsx")
mapping_file = st.file_uploader("Upload the mapping file", type="json")

if uploaded_file and mapping_file:
    try:
        import json
        mapping = json.load(mapping_file)
        validate_excel(uploaded_file, mapping)
    except Exception as e:
        st.error(f"Error processing files: {e}")
