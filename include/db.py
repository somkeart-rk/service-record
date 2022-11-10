import streamlit as st
import pymysql as connection

def init_connection():
    return connection.connect(**st.secrets["mysql"])

#conn = init_connection()

#Select data from database
def run_query(query):
    try:
        conn = init_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    finally:
        conn.close()

#Save data to database
def run_saveData(query):
    try:
        conn = init_connection()
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()
            #st.info("Save data")
    finally:
        conn.close()

def check_running(systemName,machineType):
    try:
        conn = init_connection()
        sql = f"call sms_db.check_running('{systemName}','{machineType}');"
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()
    finally:
        conn.close()

def update_running(systemName,machineType):
    try:
        conn = init_connection()
        sql = f"call sms_db.update_running('{systemName}','{machineType}');"
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    finally:
        conn.close()
