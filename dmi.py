import streamlit as st
import pandas as pd
import re
import json

def load_mapping_file(mapping_file):
    try:
        # Read the uploaded JSON file
        mapping_data = mapping_file.read()
        mapping_json = json.loads(mapping_data)
        st.write("Mapping file loaded successfully.")
        st.write("Mapping JSON:", mapping_json)  # Debugging: Show the mapping file content
        return mapping_json
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
    except Exception as e:
        st.error(f"Error loading mapping file: {e}")
    return None

def extract_flat_file_headers(properties, parent_key=''):
    headers = []
    for key, value in properties.items():
        if 'flatFileHeader' in value:
            headers.append(value['flatFileHeader'])
        if 'properties' in value:
            headers.extend(extract_flat_file_headers(value['properties'], parent_key + key + '.'))
    return headers

def validate_excel(file, mapping):
    if mapping is None:
        st.error("Mapping file is not loaded correctly.")
        return

    try:
        # Load Excel file
        df = pd.read_excel(file, engine='openpyxl')
        st.write("Excel file loaded successfully.")
        st.write("Excel Data:", df.head())  # Debugging: Show first few rows of the Excel file
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return

    try:
        # Check if 'properties' key is present
        if 'properties' not in mapping:
            st.error("Invalid mapping file: 'properties' key not found.")
            return
        
        # Extract headers from mapping
        properties = mapping['properties']
        if not isinstance(properties, dict):
            st.error("'properties' should be a dictionary.")
            return
        
        # Extract headers from the nested properties
        mapping_headers = extract_flat_file_headers(properties)
        st.write("Mapping headers extracted successfully.")
        st.write("Mapping Headers:", mapping_headers)  # Debugging: Show the extracted headers
        
    except KeyError as e:
        st.error(f"KeyError: {e}. Ensure the mapping file includes 'flatFileHeader'.")
        return
    except Exception as e:
        st.error(f"Unexpected error while processing mapping file: {e}")
        return

    # Extract headers from Excel
    headers = df.columns.tolist()
    errors = []

    # Check for missing headers
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
            # Find the field mapping for the header
            field_mapping = None
            for key, value in properties.items():
                if 'properties' in value:
                    field_mapping = find_field_mapping(value['properties'], header)
                    if field_mapping:
                        break
                elif 'flatFileHeader' in value and value['flatFileHeader'] == header:
                    field_mapping = value
                    break
            
            if field_mapping:
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

def find_field_mapping(properties, header):
    for key, value in properties.items():
        if 'flatFileHeader' in value and value['flatFileHeader'] == header:
            return value
        if 'properties' in value:
            result = find_field_mapping(value['properties'], header)
            if result:
                return result
    return None

# Streamlit UI
st.title('Excel Validation Tool')

# File uploaders for mapping file and Excel file
mapping_file = st.file_uploader("Upload your JSON mapping file", type="json")
uploaded_file = st.file_uploader("Upload your Excel file", type="xlsx")

if mapping_file and uploaded_file:
    mapping = load_mapping_file(mapping_file)
    validate_excel(uploaded_file, mapping)
