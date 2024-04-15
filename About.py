import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages



hide_pages(["Create_Account","Login","Profile","Recipes"])

st.title("PMS Chef Bot :female-cook: :seedling: ")

st.subheader("Welcome to your own menstrual cycle chef! ")

st.markdown(
    """
When I was struggling with strong PMS and irregular periods, I did not want to go back on birth control as the proposed solution, especially 
because I am trying to concieve. It took about two years measuring BBT and researching how to heal with nutrition to understand my body and finally able to have healthy cycles.

I came across a list of foods :avocado: to eat per cycles. My cycles are normally healthier with less PMS and actual ovulations when I adhere to this list.
Nutrition has a powerful affect on our bodies and I wanted this to be accessible to more people. I thought, wouldn't it be great 
to be able to look at some recipes with these ingredients customized to my:
   
    + menstrual phase 🩸
    + follicular phase 🌱
    + ovulatory phase 🥚
    + luteal phase 	🍂

Sign up and get some recommended recipes catered to your cycle phase! Happy cycle syncing! It's time to feel better, in control,
and let thy food be thy medicine. 

"""
)

if st.button("Login"):
    switch_page("Login")
if st.button("Create Account"):
    switch_page("Create_Account")
