import streamlit as st
import pandas as pd
import numpy as np
import include.db as db


@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

def color_priority(val):
    color = 'red' if val == '3-HIGH' else 'black'
    return ['color: %s' % color]

def showjob():
    st.header("งานที่กำลังทำ")
    loginName= st.session_state["userName"]
    sql = f"select priority_type,service_no,machine_no,create_date,machine_type,service_detail,status "
    sql += f" from sms_db.tbl_service_list where status='OPEN' and support_id='{loginName}' "
    sql += " order by left(priority_type,1),create_date asc ;"
    rows = db.run_query(sql)
    
    df=pd.DataFrame(rows,columns=["Priority","Job No.","Machine No.","Create Date","Machine Type","Detail","Status"])
    st.dataframe(df,use_container_width=True)

    csv = convert_df(df)
    
    st.download_button(
        "Press to Download", csv, "file.csv", "text/csv", key="download-csv"
    )
    
