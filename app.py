import streamlit as st
from streamlit_option_menu import option_menu
import pymysql as connection
#from streamlit_extras.switch_page_button import switch_page
from PIL import Image
import service_app.newjob as nj
import service_app.showjob as sj
import service_app.historyjob as hj

#st.set_page_config(layout="wide")

if "login" not in st.session_state:
    st.session_state["login"] = False
    st.session_state.userName = ""
    st.session_state.fullName = ""

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

def init_connection():
    return connection.connect(**st.secrets["mysql"])

conn = init_connection()

if not st.session_state["login"]:
    
    with st.form("login_form"):
        imgCol1,imgCol2,imgCol3 = st.columns([1.5,1,2])
        my_logo = add_logo(logo_path="./img/logo.jpg", width=206, height=122)
        imgCol2.image(my_logo,use_column_width=False)
        st.header("Login")

        userName = st.text_input("User Name")
        passWord = st.text_input("Password ","",20,None,"password")

        submitted = st.form_submit_button("Login")
        if submitted:
            #st.write(userName,":",passWord)
            if "login" in st.session_state:

                with conn.cursor() as cur:
                    #ตรวจสอบข้อมูลเจ้าหน้าที่
                    query = "select  * from sms_db.tbl_user where username='"+userName+"' and password='"+passWord+"' "
                    cur.execute(query)
                    rows = cur.fetchall()
                    if cur.rowcount:
                        st.session_state["login"] = True
                        st.session_state.userName = userName
                        for row in rows:
                            #st.write(f"{row[0]} has a :{row[1]}:")
                            st.session_state.fullName = row[1]
                            #st.write(cur)
                        st.experimental_rerun()
                    else:
                        st.info("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")

def side_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title = None,
            options = ["งานที่กำลังทำ","งานใหม่","ประวัติการซ่อม", "ตั่งค่า", "Logout"],
            icons = ["list-task","file","book","gear","key"],
            menu_icon = "cast",
            default_index = 0,
            #orientation = "horizontal",
            styles={
                    "container": {"padding": "0!important", "background-color": "#0a0afa"},
                    "icon": {"color": "orange", "font-size": "16px"}, 
                    "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "green"},
                }
        )
        if "login" in st.session_state:
            st.write('User Name : ',st.session_state["userName"] )
            st.write('Emp Name  : ',st.session_state["fullName"] )

    if selected == "งานใหม่":
        nj.newjob()
    if selected == "งานที่กำลังทำ":
        sj.showjob()
    if selected == "ประวัติการซ่อม":
        hj.showhistiryjob()
    if selected == "Logout":
        with st.form("logout_form"):
            st.header("Logout")
            st.write("Confirme Logout")

            submitted = st.form_submit_button("Logout")
            if submitted:
                if "login" in st.session_state:
                    st.session_state["login"] = False
                    st.experimental_rerun()


if st.session_state["login"]:
    side_menu()

st.write(st.session_state["login"])

