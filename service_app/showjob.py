import time
import numpy as np
import pandas as pd
import streamlit as st
import service_app.newjob as nj
import include.db as db


#@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")

def color_priority(val):
    color = 'red' if val == '3-HIGH' else 'black'
    return 'color:{}'.format(color)   

def showjob():
    st.header("งานที่กำลังทำ")
    loginName= st.session_state["userName"]
    # # Show user table 
    colms = st.columns((0.35, 0.75, 0.75, 2, 0.75))
    fields = ["№", 'เลขที่งาน', 'เครื่องจักร', 'อาการ', 'สถานะ']
    for col, field_name in zip(colms, fields):    # header
        col.write(field_name)

    sql = f"select service_list_id,service_no,machine_no,service_detail,status "
    sql += f" from sms_db.tbl_service_list where status='OPEN' and support_id like '{loginName}' "
    sql += " order by left(priority_type,1) desc,create_date asc ;"
    rows = db.run_query(sql)
    service_table=pd.DataFrame(rows,columns=["№","service_no","machine_no","service_detail","status"])

    for x, service_no in enumerate(service_table['service_no']):
        col1, col2, col3, col4, col5 = st.columns((0.35, 0.75, 0.75, 2, 0.75))
        col1.write(x)  
        col2.write(service_table['service_no'][x])  
        col3.write(service_table['machine_no'][x])  
        col4.write(service_table['service_detail'][x])  
        disable_status = service_table['status'][x]  
        button_type = "Close" if disable_status else "OPEN"
        button_phold = col5.empty()  
        do_action = button_phold.button(button_type, key=x)
        if do_action:
            button_phold.empty()  
            serviceNo = service_table['service_no'][x]
            nj.Closejob(service_no)

    csv = convert_df(service_table)
    st.download_button(
        "กดเพื่อบันทึกไฟล์", csv, "file.csv", "text/csv", key="download-csv"
    )
    
