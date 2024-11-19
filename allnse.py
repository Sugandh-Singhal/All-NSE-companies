import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the Excel file
    excel_file = pd.ExcelFile(uploaded_file)

    # Check if required sheets exist
    required_sheets = ["Nse", "Indices"]
    missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_file.sheet_names]

    if missing_sheets:
        st.error(f"The following required sheets are missing: {', '.join(missing_sheets)}")
    else:
        # Load the specific sheets into DataFrames
        nse = pd.read_excel(excel_file, sheet_name="Nse")
        indices = pd.read_excel(excel_file, sheet_name="Indices")
        
    
#file_path = "C:/Users/sugan/Downloads/NSE Companies.xlsx"  # Replace with the actual file path

# Load the individual sheets into separate DataFrames
#sheet1_name = "Nse"  # Replace with the name of your first sheet
#sheet2_name = "Indices"  # Replace with the name of your second sheet

# Read the sheets
#nse = pd.read_excel(file_path, sheet_name=sheet1_name)
#indices = pd.read_excel(file_path, sheet_name=sheet2_name)

# Extract unique values from the 'Index' column in Sheet2
unique_indexes = indices["Index"].unique()

# Streamlit app
st.title("All NSE Companies")

# Create radio button for unique Index values
selected_index = st.radio("Select an Index:", unique_indexes)

# Filter Sheet2 for the selected index
filtered_sheet2 = indices[indices["Index"] == selected_index]

# Extract the symbols corresponding to the selected index
symbols = filtered_sheet2["Symbol"].unique()

# Filter Sheet1 for the extracted symbols
filtered_sheet1 = nse[nse["Symbol"].isin(symbols)].reset_index(drop=True)

# st.write(f"Filtered Data on the basis of '{selected_index}':")
# st.dataframe(filtered_sheet1)

unique_industries = filtered_sheet1["Industry"].unique()

# Create a multiselect dropdown for industries
selected_industries = st.multiselect(
    "Filter by Industry:",
    options=unique_industries,
    default=unique_industries,  # Default to all industries selected
)

# Filter the data further based on selected industries
if selected_industries:
    filtered_sheet1 = filtered_sheet1[filtered_sheet1["Industry"].isin(selected_industries)].reset_index(drop=True)

# Display the filtered data
st.write(f"Filtered Data for '{selected_index}' and Selected Industries:")
st.dataframe(filtered_sheet1)

# Assuming 'filtered_sheet1' is your DataFrame
# Ensure 'Industry' and 'Market Cap' columns are present



if "Industry" in filtered_sheet1.columns and "Market Capitalization" in filtered_sheet1.columns:
    # Get the rows with the highest Market Cap in each Industry
    top_companies = (
        filtered_sheet1.loc[
            filtered_sheet1.groupby("Industry")["Market Capitalization"].idxmax()
        ]
        .reset_index(drop=True)
    )

    # Display the result
    st.write("Top Companies by Market Cap in Each Industry:")
    st.dataframe(top_companies, use_container_width=True)
else:
    st.error("The columns 'Industry' and 'Market Cap' are not present in the DataFrame.")
