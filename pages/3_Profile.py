import streamlit as st
from st_pages import Page, show_pages, hide_pages
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

# if 'cache' not in st.session_state:
#     cursor = get_cycle_info()
#     for record in cursor:
#         st.session_state.cache = {'last_cycle_date': record["last_cycle_date"], 'period_length': record["period_length"], 'luteal_length': record["luteal_length"],"cycle_length":record["cycle_length"]}

hide_pages(["Create_Account","Login"])


#email = st.session_state["email"]
#pwd_hashed = st.session_state["pwd_hashed"]

st.header("Welcome to your Profile")#

st.subheader("Below are your cycle stats that you have provided.")

tmp_cycle_info = pd.read_csv('tmp_cycle_info.csv',infer_datetime_format=True)


tmp_cycle_info['last_cycle_date'] = pd.to_datetime(tmp_cycle_info['last_cycle_date'] )
tmp_cycle_info['today'] =  pd.Timestamp.utcnow() 
tmp_cycle_info['cycle_day'] = (tmp_cycle_info["today"] - tmp_cycle_info["last_cycle_date"]).dt.days

cycle_day = tmp_cycle_info['cycle_day'].values[0]
period_length = tmp_cycle_info['period_length'].values[0]
cycle_length = tmp_cycle_info['cycle_length'].values[0]


if cycle_day > 40 or cycle_length < cycle_day:
    last_cycle_date = st.date_input("Please update your latest cycle")
    if st.button("Submit"):
        #st.write(type(last_cycle_date))
        tmp_cycle_info['last_cycle_date_updated'] = pd.to_datetime(last_cycle_date,utc=True)
        #st.write(tmp_cycle_info.dtypes)
        tmp_cycle_info['cycle_day'] = (tmp_cycle_info["today"] - tmp_cycle_info["last_cycle_date_updated"]).dt.days
        cycle_day = tmp_cycle_info['cycle_day'].values[0]
        st.dataframe(tmp_cycle_info)
        if (cycle_length  - cycle_day) < period_length:
            phase = 'Menstrual'
        elif cycle_day < period_length:
            phase = 'Menstrual'
        elif cycle_day > period_length and cycle_day < 13:
            phase = 'Follicular'
        elif cycle_day >= 13 and cycle_day < 19:
            phase = 'Ovulatory'
        else:
            phase = 'Luteal'
        if phase:
            file =  open("tmp_phase.txt","w")
            file.write(f"{phase} Phase") 
            file.close()

        st.subheader(f" According to your cycle info, you are in your {phase.lower()} phase")
        # with open("tmp_phase.txt","r") as f:
        #     phase = f.readlines()
        #     phase = phase[0]
        #     f.close()
        # if st.button(f"Go to Recipes for your {phase}"):
        #     switch_page("Recipes")
 
else:
    st.dataframe(tmp_cycle_info)
    if (cycle_day  - cycle_length) < period_length:
        phase = 'Menstrual'
    elif cycle_day < period_length:
        phase = 'Menstrual'
    elif cycle_day > period_length and cycle_day < 14:
        phase = 'Follicular'
    elif cycle_day > 14 and cycle_day < 19:
        phase = 'Ovulatory'
    else:
        phase = 'Luteal'
    if phase:
        file =  open("tmp_phase.txt","w")
        file.write(f"{phase} Phase") 
        file.close()

    st.subheader(f" According to your cycle info, you are in your {phase.lower()} phase")
    
with open("tmp_phase.txt","r") as f:
    phase = f.readlines()
    phase = phase[0]
    f.close()
if st.button(f"Go to Recipes for your {phase}"):
    switch_page("Recipes")



