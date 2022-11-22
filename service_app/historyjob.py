from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np 
import pymysql as connection
import include.db as db
import include.export_tools as exp


# Cache the dataframe so it's only loaded once
@st.experimental_memo
def load_data(startDate,finishDate,machineType,machineNo):
    sql = "select t0.service_no,t0.machine_no,t0.service_detail,t0.support_id,t1.finish_date "
    sql += " from sms_db.tbl_service_list t0,sms_db.tbl_service_detail t1 "
    sql += " where t0.service_no = t1.service_no and t0.status = 'CLOSE' "
    if machineType:
        sql += f" and t0.machine_type='{machineType}' "
    if machineNo:
        sql += f" and t0.machine_no='{machineNo}' "
    if startDate and finishDate:
        sql += f" and (date_format(t1.finish_date,'%Y-%m-%d') between date'{startDate}' and '{finishDate}' ) "
    sql += " order by t1.finish_date desc; "
    rows = db.run_query(sql)
    return pd.DataFrame(rows,columns=["Service No","Machine No","Service Detail","Support ID","Finish Date"])
    
def showhistiryjob():
    st.header("ประวัติการซ่อม")

    col1, col2,col3,col4,col5 = st.columns([1,1,1,1,1])

    st_d = col1.date_input("วันที่เริ่ม")
    fn_d = col2.date_input("วันสุดท้าย")
    machineType = col3.selectbox("ประเภทเครื่องจักร",db.load_machineType())
    machineNo = col4.text_input("หมายเลขเครื่อง")

    if col5.button("ค้นหา"):
        #st.write(st_d," ",fn_d)
        df = load_data(st_d,fn_d,machineType,machineNo)
        st.dataframe(df, use_container_width=True)
        st.download_button(label="download as Excel-file",
            data=exp.convert_to_excel(df),
            file_name="export_history.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="excel_download",
        )

    else:
        st.write('Not Select')




    