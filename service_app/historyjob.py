from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np 
import pymysql as connection
import include.db as db

# Cache the dataframe so it's only loaded once
@st.experimental_memo
def load_data():
    return pd.DataFrame(
        {
            "first column": [1, 2, 3, 4],
            "second column": [10, 20, 30, 40],
        }
    )

 
def showhistiryjob():
    st.header("ประวัติการซ่อม")

    col1, col2,col3,col4,col5 = st.columns([1,1,1,1,1])

    st_d = col1.date_input("วันที่เริ่ม")
    fn_d = col2.date_input("วันสุดท้าย")
    machineType = col3.selectbox("ประเภทเครื่องจักร",["KNIT","DYE","SPUN"])
    machineNo = col4.text_input("หมายเลขเครื่อง")

    if col5.button("ค้นหา"):
        st.write(st_d," ",fn_d)
    else:
        st.write('Not Select')


    # Boolean to resize the dataframe, stored as a session state variable
    #st.checkbox("Use container width", value=False, key="use_container_width")

    df = load_data()

    # Display the dataframe and allow the user to stretch the dataframe
    # across the full width of the container, based on the checkbox value
    st.dataframe(df, use_container_width=True)


    