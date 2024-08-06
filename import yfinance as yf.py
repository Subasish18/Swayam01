import yfinance as yf
import streamlit as st
import pandas as pd
import datetime

st.write("""
         #Stock pric app
         
         shown are the **volume** of Google""")
A = datetime.datetime.now()
G = "GOOGL"
D = yf.Ticker(G)
DF = D.history(period = '1d',start = "2010-01-01",end = A)

st.line_chart(DF.Volume)
st.bar_chart(DF.Volume)
