import streamlit as st
from st_pages import Page, show_pages, hide_pages

hide_pages(["Create_Account","Profile_Recipes"])


username= st.text_input(":red[Username]",key="username",max_chars=25,help='required')
pwd = st.text_input(":red[Password]",key="pwd",type='password',max_chars=15,help='required')


