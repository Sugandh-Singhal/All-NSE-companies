import streamlit as st
import pandas as pd

file_path = "C:/Users/sugan/Downloads/NSE Companies.xlsx"  # Replace with the actual file path

# Load the individual sheets into separate DataFrames
sheet1_name = "Nse"  # Replace with the name of your first sheet
sheet2_name = "Indices"  # Replace with the name of your second sheet

# Read the sheets
nse = pd.read_excel(file_path, sheet_name=sheet1_name)
indices = pd.read_excel(file_path, sheet_name=sheet2_name)

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
