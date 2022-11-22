from io import BytesIO
import pandas as pd
import streamlit as st
import xlsxwriter

def convert_to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="export data")

    # you can do all sorts of formating here 
    # see: https://xlsxwriter.readthedocs.io/working_with_pandas.html

    writer.save()
    
    return output.getvalue()

@st.experimental_memo
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")
