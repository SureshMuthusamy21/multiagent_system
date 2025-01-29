import streamlit as st
import asyncio
from config.config import Config
from main import main

st.set_page_config(layout="wide")
st.title("Stock Analysis Comparison")

# Input widgets
col1, col2 = st.columns(2)

with col1:
    symbol1 = st.text_input("First Stock Symbol", value=Config.SYMBOLS[0])
    
with col2:
    symbol2 = st.text_input("Second Stock Symbol", value=Config.SYMBOLS[1])

period = st.selectbox(
    "Select Time Period",
    options=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    index=2  # Default to "1mo"
)

if st.button("Analyze Stocks"):
    # Update config
    Config.SYMBOLS = [symbol1, symbol2]
    Config.PERIOD = period
    
    # Run analysis
    with st.spinner('Analyzing stocks...'):
        results = asyncio.run(main())
        
        # Display results side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.header(f"Analysis for {results[0]['symbol']}")
            
            st.subheader("Company Information")
            st.json(results[0]['company_info'])
            
            st.subheader("Stock Data")
            st.dataframe(results[0]['stock_data'])
            
            st.subheader("Fundamental Analysis")
            st.markdown(results[0]['fundamental_analysis'])
            
            st.subheader("Technical Analysis")
            st.markdown(results[0]['technical_analysis'])
            
        with col2:
            st.header(f"Analysis for {results[1]['symbol']}")
            
            st.subheader("Company Information")
            st.json(results[1]['company_info'])
            
            st.subheader("Stock Data")
            st.dataframe(results[1]['stock_data'])
            
            st.subheader("Fundamental Analysis")
            st.markdown(results[1]['fundamental_analysis'])
            
            st.subheader("Technical Analysis")
            st.markdown(results[1]['technical_analysis']) 