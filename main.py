import streamlit as st
import time
import random
import secrets
import datetime

# Инициализация состояния
if 'user_id' not in st.session_state:
    st.session_state.user_id = secrets.token_hex(8)
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'cps' not in st.session_state:
    st.session_state.cps = 0
if 'cpc' not in st.session_state:
    st.session_state.cpc = 1
if 'upgrades' not in st.session_state:
    st.session_state.upgrades = {
        "fedorov_ml": 0,
        "fedorov_str": 0,
        "korneeva": 0,
        "epihin": 0,
        "zharkova": 0,
        "sokolova": 0,
        "kozhukhov": 0,
        "novikov": 0,
        "harach": 0,
        "volkov": 0
    }
if 'last_bonus_time' not in st.session_state:
    st.session_state.last_bonus_time = None


upgrades_info = {  "fedorov_ml": {"name": "Федоров Мл.", "description": "Дает 10000 бонусов в неделю", "cost": 100000, "cps": 0, "weekly_bonus": 10000, "image": "default.png"},
    "fedorov_str": {"name": "Федоров Стр.", "description": "+20 кликов в секунду", "cost": 2500, "cps": 20, "weekly_bonus": 0, "image": "default.png"},
    "korneeva": {"name": "Корнеева", "description": "+50 кликов в секунду", "cost": 5, "cps": 50, "weekly_bonus": 0, "image": "default.png"},
    "epihin": {"name": "Епихин", "description": "+10 кликов в секунду", "cost": 1000, "cps": 10, "weekly_bonus": 0, "image": "default.png"},
    "zharkova": {"name": "Жаркова", "description": "+60 кликов в секунду", "cost": 25000, "cps": 60, "weekly_bonus": 0, "image": "default.png"},
    "sokolova": {"name": "Соколова", "description": "+15 кликов в секунду", "cost": 800, "cps": 15, "weekly_bonus": 0, "image": "default.png"},
    "kozhukhov": {"name": "Кожухов", "description": "+1 клик за клик", "cost": 10, "cpc": 1, "weekly_bonus": 0, "image": "default.png"},
    "novikov": {"name": "Новиков", "description": "+70 кликов в секунду", "cost": 10000, "cps": 70, "weekly_bonus": 0, "image": "default.png"},
    "harach": {"name": "Харач", "description": "+2 клика в секунду и +10000 бонусов в неделю", "cost": 15000, "cps": 2, "weekly_bonus": 10000, "image": "default.png"},
    "volkov": {"name": "Волков", "description": "+5 кликов в секунду", "cost": 13500, "cps": 5, "weekly_bonus": 0, "image": "default.png"}}

upgrade_names = list(upgrades_info.keys())

def give_weekly_bonus():
    now = datetime.datetime.now()
    if st.session_state.last_bonus_time:
        time_diff = now - st.session_state.last_bonus_time
        if time_diff >= datetime.timedelta(days=7):
            bonus = 0
            for upgrade_name in upgrade_names:
                if st.session_state.upgrades[upgrade_name] == 1 and upgrades_info[upgrade_name].get('weekly_bonus'):
                    bonus += upgrades_info[upgrade_name]['weekly_bonus']
            st.session_state.count += bonus
            st.session_state.last_bonus_time = now
    else:
       #give immediately the first time

        bonus = 0
        for upgrade_name in upgrade_names:



          if st.session_state.upgrades[upgrade_name] == 1 and upgrades_info[upgrade_name].get('weekly_bonus'):



            bonus += upgrades_info[upgrade_name]['weekly_bonus']

        st.session_state.count+=bonus


        st.session_state.last_bonus_time = datetime.datetime.now()


def update_count_with_cps():
    cps = 0
    for upgrade_name in upgrade_names:
        if st.session_state.upgrades[upgrade_name]:
            cps += upgrades_info[upgrade_name].get('cps', 0)
    st.session_state.count += cps
    st.session_state.cps = cps # Update cps in session state
    return cps

def increment():
    st.session_state.count += st.session_state.cpc


#update on start if necessary
update_count_with_cps()




st.title("Simple Clicker")
st.write(f"Count: {st.session_state.count}")



st.button("Click me!", on_click=increment)




st.write(f"Clicks per second: {st.session_state.cps}")



# Автоматический кликер



placeholder = st.empty()

i = 0


def auto_click():

    give_weekly_bonus() # Weekly bonuses
    update_count_with_cps()



    i+=1

    placeholder.text(f'{st.session_state.count}')






auto_click()

# Auto-clicker using Streamlit's built-in rerun feature
st.experimental_rerun()





# Shop




st.title('Магазин')


for upgrade_name, upgrade in upgrades_info.items():
  if st.session_state.upgrades[upgrade_name] == 0:
        if st.button(f"Buy {upgrade['name']} for {upgrade['cost']}"):


            can_buy = st.session_state.count >= upgrade['cost']


            if can_buy:


               st.session_state.upgrades[upgrade_name] = 1


               st.session_state.count =  st.session_state.count- upgrade['cost']


               st.session_state.cpc = st.session_state.cpc+ upgrade.get('cpc', 0) # apply clicks per click bonuses if any

               update_count_with_cps()

               st.experimental_rerun()



            else:



              st.write("you cannot buy this yet.")








# Display updated values


st.write("Your orioks now:"+str(st.session_state.count))




for upgrade in upgrade_names:


   if st.session_state['upgrades'][upgrade] == 1:
       st.write("Your purchased widget: " + upgrade)