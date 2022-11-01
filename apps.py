# from tkinter import Menu
import streamlit as st
from streamlit_option_menu import option_menu


def side_menu():
    #st.sidebar.image("./images/tsc_logo2.jpg",width=100)
    with st.sidebar:
        selected = option_menu(
            menu_title = "Main Menu",
            options = ["Home","Projects","Contact"],
            icons = ["house","book","envelope"],
            menu_icon = "cast",
            default_index = 0,
            #orientation = "horizontal",
        )
    
    if selected == "Home":
        st.title(f"You have selected {selected}")
    if selected == "Projects":
        st.title(f"You have selected {selected}")
    if selected == "Contact":
        st.title(f"You have selected {selected}")

    #st.sidebar.image("https://static.streamlit.io/examples/owl.jpg")
    st.sidebar.title('MENU')
    st.sidebar.write('1.')
    genre = st.sidebar.radio(
        "What's your favorite movie genre",
        ( 'Drama', 'Comedy', 'Documentary'))

    if genre == 'Comedy':
        st.write('You selected comedy.')
        st.balloons()
    else:
        st.write("You didn't select comedy.")


def main_view():
    col1, col2 = st.columns([2,10])
    with col1:
        st.button("เปลี่ยนลาย")

    with col2:
        st.button("ทำความสะอาดเครื่อง")

    if st.button('Say hello'):
        st.write('Why hello there')
    else:
        st.write('Goodbye')


side_menu()
main_view()

with st.form("my_form"):
   st.write("Inside the form")
   slider_val = st.slider("Form slider")
   checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("slider", slider_val, "checkbox", checkbox_val)
       if slider_val == 50:
            st.balloons()

st.write("Outside the form")
