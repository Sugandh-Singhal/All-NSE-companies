import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

# Streamlit file uploader
uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx"], accept_multiple_files=True)

# Check if files are uploaded
if uploaded_files:
    # Ensure two files are uploaded
    if len(uploaded_files) == 2:
        # Load the first file into a DataFrame
        nse = pd.read_excel(uploaded_files[0])
        
        # Load the second file into a DataFrame
        indices = pd.read_excel(uploaded_files[1])
        
        # Extract unique values from the 'Index' column in Sheet1 (nse)
        unique_indexes = indices["Index"].unique()
        
        # Streamlit app title
        st.title("All NSE Companies")
        
        # Create radio button for unique Index values
        selected_index = st.radio("Select an Index:", unique_indexes)
        
        # Filter Sheet2 (indices) for the selected index
        filtered_sheet2 = indices[indices["Index"] == selected_index]
        
        # Extract the symbols corresponding to the selected index
        symbols = filtered_sheet2["Symbol"].unique()
        
        # Filter Sheet1 (nse) for the extracted symbols
        filtered_sheet1 = nse[nse["Symbol"].isin(symbols)].reset_index(drop=True)
        
        # Display the filtered data
        st.write(f"Filtered Data based on Index '{selected_index}':")
        st.dataframe(filtered_sheet1)
        
        # Extract unique industries from filtered data
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
        
        # Display the filtered data after industry filtering
        st.write(f"Filtered Data for '{selected_index}' and Selected Industries:")
        st.dataframe(filtered_sheet1)
        
        # Check if 'Industry' and 'Market Capitalization' columns exist
        if "Industry" in filtered_sheet1.columns and "Market Capitalization" in filtered_sheet1.columns:
            # Get the rows with the highest Market Cap in each Industry
            top_companies = (
                filtered_sheet1.loc[
                    filtered_sheet1.groupby("Industry")["Market Capitalization"].idxmax()
                ]
                .reset_index(drop=True)
            )
            
            # Display the top companies
            st.write("Top Companies by Market Cap in Each Industry:")
            st.dataframe(top_companies, use_container_width=True)
        else:
            st.error("The columns 'Industry' and 'Market Capitalization' are not present in the DataFrame.")
    
    else:
        st.error("Please upload exactly two files. One for NSE data and one for indices.")
