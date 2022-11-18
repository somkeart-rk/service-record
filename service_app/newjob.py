import streamlit as st
import pandas as pd
import include.db as db
import time

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


def Closejob(service_No):
    CloseJob_form = st.form(key="Close Job")
    if 'pChange' not in st.session_state:
        st.session_state.pChange=' '
        st.session_state.sDetail=' '

    CloseJob_form.subheader("บันทึกรายละเอียดการซ่อม")
    serviceGroup = CloseJob_form.selectbox(f"ประเภทการซ่อม",["เปลี่ยนเข็ม","ปรับตั้งเครื่อง"])
    CloseJob_form.text_input("อุปกรณ์ที่เปลี่ยน",key="pChange",value="Needle",max_chars=199 )
    CloseJob_form.text_area(f"รายละเอียดการซ่อม",key="sDetail",value="144",max_chars=1000)
    CloseJob_form.form_submit_button("ปิดงานซ่อม",on_click=saveData,args=[service_No,serviceGroup,])


def saveData(service_No,serviceGroup,):
    partChange = st.session_state.pChange
    serviceDetail = st.session_state.sDetail
    sqlUpdate = f"UPDATE `sms_db`.`tbl_service_list` SET `status`= 'CLOSE' WHERE `service_no`='{service_No}'; "
    #st.write(sqlUpdate)
    db.run_saveData(sqlUpdate)

    sqlAddDetail = "INSERT INTO `sms_db`.`tbl_service_detail`(`service_no`,`service_group`,`part_detail`,`service_detail`) "
    sqlAddDetail += f" VALUES('{service_No}','{serviceGroup}','{partChange}','{serviceDetail}'); "
    #st.write(sqlAddDetail)
    db.run_saveData(sqlAddDetail)
    st.info(f"งานหมายเลข : {service_No} ปิดเรียบร้อย")
    #time.sleep(0.5)
 