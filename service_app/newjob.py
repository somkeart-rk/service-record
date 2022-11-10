import streamlit as st
import pandas as pd
import include.db as db

def newjob():
    with st.form("new_form"):
        st.header("เปิดงานใหม่")
        col1,col2,col3 = st.columns(3)
        machineType = col1.selectbox("ประเภทเครื่องจักร",["KNIT","DYE","SPUN"])
        machineNo = col2.text_input("หมายเลขเครื่อง")
        priority = col3.selectbox("ความเร่งด่วนของงาน",["1-LOW","2-MEDIUM","3-HIGH"])
        serviceDetail = st.text_area("ปัญหาก่อนซ่อม")

        submitted = st.form_submit_button("เปิดงานใหม่")
        if submitted:
            loginName= st.session_state["userName"]
            #Check running data from server
            rows = db.check_running(systemName="SERVICE",machineType=machineType)
            for row in rows:
                jobRunning = row[0]

            #update running to database
            db.update_running(systemName="SERVICE",machineType=machineType)

            sql = "INSERT INTO `sms_db`.`tbl_service_list`(`service_no`,`machine_type`,`machine_no`,"
            sql += "`priority_type`,`service_detail`,`user_create`,`support_id`) "
            sql += f" VALUES('{jobRunning}','{machineType}','{machineNo}','{priority}','{serviceDetail}','{loginName}','{loginName}' ); "
            #st.write(sql)
            db.run_saveData(sql)

            #save data into database
            st.info(f"Job No# : {jobRunning} has been created.")

        st.write("ประวัติการซ่อม")

