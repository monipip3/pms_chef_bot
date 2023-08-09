import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages



hide_pages(["Create_Account","Login","Profile"])

st.title("PMS Chef Bot :female-cook: :seedling: ")

st.subheader("Welcome to your own menstrual cycle chef! ")

st.markdown(
    """
When I wanted to take the IUD early to one day become pregnant :pregnant_woman: ,I was brought back to my pre IUD self and 
had to deal with all this terrible PMS, heavy periods, a menstrual cycle of 35-40 days.I almost laughed when one of the nurses at my OBYGYN practice said Birth control would fix it.

I knew she meant well and that doctors spent 1% of their medical field on nutrition but I started reading content from holistic doctors using nutrition to appease hormone imbalances. 

I did not want to suppress these symptoms like a bandaid. I wanted to get to the root :seedling: of my hormone imbalance.

Fast forward months of researching and changing some eating habits and I had periods under 35 days that were more 
predictable, confirmed ovulations from BBT, and less signs of PMS. 
I know most of it was learning about cycle syncing with food because I was nourishing my body the nutrients it needed to have
a healthier period. 

It was not until I came across a list of foods :avocado: to eat per cycles that I thought, wouldn't it be great 
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