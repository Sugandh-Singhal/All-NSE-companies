import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    # Load the uploaded Excel file into a pandas ExcelFile object
    excel_file = pd.ExcelFile(uploaded_file)

    # Check if the required sheets exist in the uploaded Excel file
    required_sheets = ["Nse", "Indices"]
    missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_file.sheet_names]

    if missing_sheets:
        st.error(f"The following required sheets are missing: {', '.join(missing_sheets)}")
    else:
        # Load the specific sheets into DataFrames
        nse = pd.read_excel(excel_file, sheet_name="Nse", engine="openpyxl")
        indices = pd.read_excel(excel_file, sheet_name="Indices", engine="openpyxl")

        # Extract unique values from the 'Index' column in the 'Nse' DataFrame
        unique_indexes = indices["Index"].unique()

        # Create radio button for unique Index values
        selected_index = st.radio("Select an Index:", unique_indexes)

        # Filter 'Indices' DataFrame for the selected index
        filtered_sheet2 = indices[indices["Index"] == selected_index]
        
        # Extract the symbols corresponding to the selected index
        symbols = filtered_sheet2["Symbol"].unique()

        # Filter 'Nse' DataFrame for the extracted symbols
        filtered_sheet1 = nse[nse["Symbol"].isin(symbols)].reset_index(drop=True)


        # Extract unique industries from filtered data
        unique_industries = filtered_sheet1["Industry"].unique()


# Create a multiselect dropdown with customized label
        selected_industries = st.multiselect(
            "# **Filter by Industry:**",
            options=unique_industries,  # Default to all industries selected
            )


        # Filter the data further based on selected industries
        if selected_industries:
            filtered_sheet1 = filtered_sheet1[filtered_sheet1["Industry"].isin(selected_industries)].reset_index(drop=True)

        # Display the filtered data after industry filtering
        st.title(f"Filtered Data for '{selected_index}' and Selected Industries:")
        st.dataframe(filtered_sheet1)

        # Ensure 'Industry' and 'Market Capitalization' columns are present
        if "Industry" in filtered_sheet1.columns and "Market Capitalization" in filtered_sheet1.columns:
            # Get the rows with the highest Market Cap in each Industry
            top_companies = (
                filtered_sheet1.loc[
                    filtered_sheet1.groupby("Industry")["Market Capitalization"].idxmax()
                ]
                .reset_index(drop=True)
            )

            # Display the result
            st.title("Top Companies by Market Cap in Each Industry:")
            st.dataframe(top_companies, use_container_width=True)
        else:
            st.error("The columns 'Industry' and 'Market Capitalization' are not present in the DataFrame.")
            
        import plotly.express as px

# Group by industry and sum the market capitalization
        industry_market_cap = filtered_sheet1.groupby('Industry')['Market Capitalization'].sum().reset_index()
        
        # Sort the data in descending order based on 'Market Capitalization'
        industry_market_cap = industry_market_cap.sort_values(by='Market Capitalization', ascending=False)

# Create a bar chart
        fig = px.bar(industry_market_cap, x='Industry', y='Market Capitalization',
                     title='Market Capitalization by Industry',
                     labels={'Market Capitalization': 'Market Capitalization (in Crores)'})
        
        fig.update_layout(
            width=1400,  # Set the width of the graph (increase as needed)
            height=800,  # Set the height of the graph (increase as needed)
            title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        )
        # Show the chart in Streamlit
        st.plotly_chart(fig)
    
        industry_count = filtered_sheet1['Industry'].value_counts().reset_index()
        industry_count.columns = ['Industry', 'Count']
        
        # Create bar chart
        fig = px.bar(industry_count, x='Industry', y='Count',
                     title='Distribution of Companies by Industry',
                     labels={'Count': 'Number of Companies'})
        fig.update_layout(
            width=1400,  # Set the width of the graph (increase as needed)
            height=800,  # Set the height of the graph (increase as needed)
            title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        )
        # Show the chart in Streamlit
        st.plotly_chart(fig)
        

        industry_roe = filtered_sheet1.groupby('Industry')['Return on equity'].mean().reset_index()
        
        # Sort the data in descending order based on 'Return on equity'
        industry_roe = industry_roe.sort_values(by='Return on equity', ascending=False)
        
        # Create a bar chart
        fig = px.bar(industry_roe, x='Industry', y='Return on equity',
                     title='Average Return on Equity by Industry',
                     labels={'Return on equity': 'Average Return on Equity (%)'})
        
        # Increase graph size
        fig.update_layout(
            width=1400,  # Set the width of the graph (increase as needed)
            height=800,  # Set the height of the graph (increase as needed)
            title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        )
        
        # Show the chart in Streamlit
        st.plotly_chart(fig)
else:
    st.info("Please upload an Excel file.")