import streamlit as st
import pandas as pd
import re
import json

# Load mapping file
def load_mapping_file(mapping_file_path):
    try:
        with open(mapping_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading mapping file: {e}")
        return None

# Validate header and values
def validate_excel(file, mapping):
    if mapping is None:
        st.error("Mapping file is not loaded correctly.")
        return

    # Load Excel file
    try:
        df = pd.read_excel(file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return

    # Extract headers
    headers = df.columns.tolist()
    errors = []

    # Check for missing headers
    if 'properties' not in mapping:
        st.error("Invalid mapping file: 'properties' key not found.")
        return

    mapping_headers = {field['flatFileHeader'] for field in mapping['properties'].values()}
    missing_headers = [header for header in mapping_headers if header not in headers]
    if missing_headers:
        errors.append(f"Missing headers: {', '.join(missing_headers)}")

    # Check for extra headers
    extra_headers = [header for header in headers if header not in mapping_headers]
    if extra_headers:
        errors.append(f"Extra headers: {', '.join(extra_headers)}")

    # Check for incorrect values in the fields
    for header in headers:
        if header in mapping_headers:
            field_mapping = next(field for key, field in mapping['properties'].items() if field['flatFileHeader'] == header)
            pattern = field_mapping.get('pattern', None)
            if pattern:
                regex = re.compile(pattern)
                for i, value in enumerate(df[header]):
                    if pd.notna(value) and not regex.match(str(value)):
                        errors.append(f"Invalid value '{value}' in header '{header}' at row {i+1}. Expected format: {pattern}")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.success("All headers and values are correct.")

# Streamlit UI
st.title('Excel Validation Tool')
uploaded_file = st.file_uploader("Upload your Excel file", type="xlsx")

if uploaded_file:
    mapping_file_path = 'loan_create_or_update.json'  # Ensure this path is correct and file is included in your repository
    mapping = load_mapping_file(mapping_file_path)
    validate_excel(uploaded_file, mapping)
