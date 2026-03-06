# JSON ↔ Excel/CSV Converter

A simple and intuitive Streamlit web application for converting between JSON, Excel (.xlsx, .xls), and CSV file formats.

## Features

- ✅ **JSON to Excel** - Convert JSON files/objects to Excel spreadsheets
- ✅ **JSON to CSV** - Convert JSON files/objects to CSV files
- ✅ **Excel to JSON** - Convert Excel spreadsheets to JSON format
- ✅ **Excel to CSV** - Convert Excel spreadsheets to CSV format
- ✅ **CSV to JSON** - Convert CSV files to JSON format
- ✅ **CSV to Excel** - Convert CSV files to Excel spreadsheets

## Installation

1. Clone this repository:
```bash
git clone https://github.com/CraneCD/json-excel-converter.git
cd json-excel-converter
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

### How to Use

1. Select the conversion type from the dropdown menu
2. Choose your input method:
   - **Upload File**: Upload a file from your computer
   - **Manual Input**: Paste JSON data directly (only for JSON input)
3. Preview your data
4. Download the converted file

## Supported Formats

- **JSON**: Standard JSON format (objects, arrays, nested structures)
- **Excel**: `.xlsx` and `.xls` files
- **CSV**: Comma-separated values files

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- OpenPyXL (for Excel support)
- xlrd (for older Excel file support)

## Project Structure

```
json-excel-converter/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

