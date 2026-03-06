import streamlit as st
import pandas as pd
import json
import io
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="JSON ↔ Excel/CSV Converter",
    page_icon="🔄",
    layout="wide"
)

st.title("🔄 JSON ↔ Excel/CSV Converter")
st.markdown("Convert between JSON, Excel, and CSV formats easily!")

# Sidebar for instructions
with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("""
    ### How to use:
    1. **Select conversion type** from the dropdown
    2. **Upload a file** or **enter data manually**
    3. **Download** the converted file
    
    ### Supported formats:
    - **JSON** → Excel (.xlsx) or CSV (.csv)
    - **Excel** (.xlsx, .xls) → JSON or CSV
    - **CSV** (.csv) → JSON or Excel
    
    ### Features:
    - ✅ Nested objects are automatically flattened into columns
    - ✅ Example: `{"address": {"city": "NY"}}` → `address.city` column
    - ✅ Automatically detects `data`, `results`, `items`, or `records` arrays
    """)

# Conversion type selector
conversion_type = st.selectbox(
    "Select conversion type:",
    [
        "JSON to Excel",
        "JSON to CSV",
        "Excel to JSON",
        "Excel to CSV",
        "CSV to JSON",
        "CSV to Excel"
    ]
)

st.divider()

# Function to flatten nested dictionaries
def flatten_dict(d, parent_key='', sep='.'):
    """Recursively flatten nested dictionaries"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

# Function to convert JSON to DataFrame
def json_to_dataframe(json_data):
    """Convert JSON to pandas DataFrame with nested object flattening"""
    try:
        # Try to parse as JSON string first
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        
        # Check if it's a dict with a 'data' field (or other common array field names)
        if isinstance(json_data, dict):
            # Common field names that might contain the array of objects
            array_field_names = ['data', 'results', 'items', 'records']
            
            # Check if any of these fields exist and is a non-empty list
            for field_name in array_field_names:
                if field_name in json_data:
                    field_value = json_data[field_name]
                    if isinstance(field_value, list) and len(field_value) > 0:
                        # Found an array - use it for conversion
                        if isinstance(field_value[0], dict):
                            # Use pd.json_normalize to flatten nested objects
                            return pd.json_normalize(field_value)
                        else:
                            # List of values
                            return pd.DataFrame(field_value, columns=[field_name])
            
            # If it's a dict, check if values are lists/arrays
            if all(isinstance(v, list) and len(v) > 0 for v in json_data.values() if isinstance(v, list)):
                # Standard dict with lists as values - try json_normalize first
                try:
                    return pd.json_normalize(json_data)
                except:
                    # Fallback to regular DataFrame
                    return pd.DataFrame(json_data)
            else:
                # Single object dict - use json_normalize for better nested handling
                try:
                    return pd.json_normalize([json_data])
                except:
                    # Fallback: manually flatten and convert to single row
                    flattened = flatten_dict(json_data)
                    return pd.DataFrame([flattened])
        
        # Handle direct lists
        elif isinstance(json_data, list):
            # If it's a list of objects, use json_normalize for better nested handling
            if len(json_data) > 0 and isinstance(json_data[0], dict):
                # Use pd.json_normalize for better nested object handling
                try:
                    return pd.json_normalize(json_data)
                except:
                    # Fallback: manually flatten nested objects
                    flattened_data = [flatten_dict(item) if isinstance(item, dict) else item for item in json_data]
                    return pd.DataFrame(flattened_data)
            else:
                # List of values
                return pd.DataFrame(json_data, columns=['value'])
        else:
            st.error("Unsupported JSON structure")
            return None
    except Exception as e:
        st.error(f"Error parsing JSON: {str(e)}")
        return None

# Function to convert DataFrame to JSON
def dataframe_to_json(df, orient='records'):
    """Convert DataFrame to JSON"""
    try:
        return df.to_json(orient=orient, indent=2, date_format='iso')
    except Exception as e:
        st.error(f"Error converting to JSON: {str(e)}")
        return None

# Input section
input_method = st.radio(
    "Input method:",
    ["Upload File", "Manual Input"],
    horizontal=True
)

uploaded_file = None
input_data = None

if input_method == "Upload File":
    if "JSON" in conversion_type:
        uploaded_file = st.file_uploader(
            "Upload JSON file",
            type=['json'],
            help="Upload a JSON file to convert"
        )
    elif "Excel" in conversion_type:
        uploaded_file = st.file_uploader(
            "Upload Excel file",
            type=['xlsx', 'xls'],
            help="Upload an Excel file (.xlsx or .xls) to convert"
        )
    elif "CSV" in conversion_type:
        uploaded_file = st.file_uploader(
            "Upload CSV file",
            type=['csv'],
            help="Upload a CSV file to convert"
        )
    
    if uploaded_file:
        try:
            if "JSON" in conversion_type:
                input_data = json.load(uploaded_file)
                st.success("✅ JSON file loaded successfully!")
                with st.expander("Preview JSON"):
                    st.json(input_data)
            elif "Excel" in conversion_type:
                input_data = pd.read_excel(uploaded_file)
                st.success("✅ Excel file loaded successfully!")
                with st.expander("Preview DataFrame"):
                    st.dataframe(input_data.head(10))
            elif "CSV" in conversion_type:
                input_data = pd.read_csv(uploaded_file)
                st.success("✅ CSV file loaded successfully!")
                with st.expander("Preview DataFrame"):
                    st.dataframe(input_data.head(10))
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            input_data = None

else:  # Manual Input
    if "JSON" in conversion_type:
        st.text_area(
            "Enter JSON data:",
            height=200,
            placeholder='{"name": "John", "age": 30, "address": {"street": "123 Main St", "city": "New York"}}',
            key="json_input"
        )
        json_text = st.session_state.json_input
        if json_text:
            try:
                input_data = json.loads(json_text)
                st.success("✅ JSON parsed successfully!")
                with st.expander("Preview JSON"):
                    st.json(input_data)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {str(e)}")
                input_data = None
    elif "Excel" in conversion_type or "CSV" in conversion_type:
        st.info("💡 For Excel/CSV to JSON conversion, please use the file upload option.")

# Conversion section
if input_data is not None:
    st.divider()
    st.subheader("Converted Output")
    
    output_buffer = io.BytesIO()
    output_filename = None
    
    try:
        # JSON to Excel
        if conversion_type == "JSON to Excel":
            df = json_to_dataframe(input_data)
            if df is not None:
                df.to_excel(output_buffer, index=False, engine='openpyxl')
                output_filename = "converted_output.xlsx"
                st.dataframe(df)
        
        # JSON to CSV
        elif conversion_type == "JSON to CSV":
            df = json_to_dataframe(input_data)
            if df is not None:
                output_buffer = io.StringIO()
                df.to_csv(output_buffer, index=False)
                output_buffer = io.BytesIO(output_buffer.getvalue().encode())
                output_filename = "converted_output.csv"
                st.dataframe(df)
        
        # Excel to JSON
        elif conversion_type == "Excel to JSON":
            json_output = dataframe_to_json(input_data)
            if json_output:
                output_buffer = io.BytesIO(json_output.encode())
                output_filename = "converted_output.json"
                st.code(json_output, language='json')
        
        # Excel to CSV
        elif conversion_type == "Excel to CSV":
            output_buffer = io.StringIO()
            input_data.to_csv(output_buffer, index=False)
            output_buffer = io.BytesIO(output_buffer.getvalue().encode())
            output_filename = "converted_output.csv"
            st.dataframe(input_data)
        
        # CSV to JSON
        elif conversion_type == "CSV to JSON":
            json_output = dataframe_to_json(input_data)
            if json_output:
                output_buffer = io.BytesIO(json_output.encode())
                output_filename = "converted_output.json"
                st.code(json_output, language='json')
        
        # CSV to Excel
        elif conversion_type == "CSV to Excel":
            input_data.to_excel(output_buffer, index=False, engine='openpyxl')
            output_filename = "converted_output.xlsx"
            st.dataframe(input_data)
        
        # Download button
        if output_filename:
            output_buffer.seek(0)
            st.download_button(
                label=f"📥 Download {output_filename}",
                data=output_buffer,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if "xlsx" in output_filename else 
                     "text/csv" if "csv" in output_filename else 
                     "application/json"
            )
    
    except Exception as e:
        st.error(f"Error during conversion: {str(e)}")
        st.exception(e)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray;'>
    Made with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)

