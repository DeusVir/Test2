import streamlit as st
import time
import random
import secrets
import datetime
import sqlite3

DATABASE = 'clicker_data.db'

def init_connection():
    db = sqlite3.connect(DATABASE)
    db.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            user_id TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0,
            last_bonus_time TIMESTAMP,
            fedorov_ml INTEGER DEFAULT 0,
            fedorov_str INTEGER DEFAULT 0,
            korneeva INTEGER DEFAULT 0,
            epihin INTEGER DEFAULT 0,
            zharkova INTEGER DEFAULT 0,
            sokolova INTEGER DEFAULT 0,
            kozhukhov INTEGER DEFAULT 0,
            novikov INTEGER DEFAULT 0,
            harach INTEGER DEFAULT 0,
            volkov INTEGER DEFAULT 0
        )
    ''')
    db.commit()
    return db

def get_user_data(user_id):
    db = init_connection()
    cursor = db.cursor()
    cursor.execute("SELECT count, last_bonus_time, fedorov_ml, fedorov_str, korneeva, epihin, zharkova, sokolova, kozhukhov, novikov, harach, volkov FROM clicks WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        cursor.execute("INSERT INTO clicks (user_id) VALUES (?)", (user_id,))
        db.commit()
        return (0, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

if 'user_id' not in st.session_state:
    st.session_state.user_id = secrets.token_hex(8)

user_data = get_user_data(st.session_state.user_id)

if 'count' not in st.session_state:
    st.session_state.count = user_data[0]
if 'last_bonus_time' not in st.session_state:
    st.session_state.last_bonus_time = user_data[1]
if 'upgrades' not in st.session_state:
    upgrades = {}
    for index, upgrade_name in enumerate(upgrade_names):
        upgrades[upgrade_name] = user_data[2 + index]
    st.session_state.upgrades = upgrades
if 'cps' not in st.session_state:
    st.session_state.cps = 0
if 'cpc' not in st.session_state:
    st.session_state.cpc = 1

upgrades_info = {
    "fedorov_ml": {"name": "Федоров Мл.", "description": "Дает 10000 бонусов в неделю", "cost": 100000, "cps": 0, "weekly_bonus": 10000, "image": "default.png"},
    "fedorov_str": {"name": "Федоров Стр.", "description": "+20 кликов в секунду", "cost": 2500, "cps": 20, "weekly_bonus": 0, "image": "default.png"},
    "korneeva": {"name": "Корнеева", "description": "+50 кликов в секунду", "cost": 5, "cps": 50, "weekly_bonus": 0, "image": "default.png"},
    "epihin": {"name": "Епихин", "description": "+10 кликов в секунду", "cost": 1000, "cps": 10, "weekly_bonus": 0, "image": "default.png"},
    "zharkova": {"name": "Жаркова", "description": "+60 кликов в секунду", "cost": 25000, "cps": 60, "weekly_bonus": 0, "image": "default.png"},
    "sokolova": {"name": "Соколова", "description": "+15 кликов в секунду", "cost": 800, "cps": 15, "weekly_bonus": 0, "image": "default.png"},
    "kozhukhov": {"name": "Кожухов", "description": "+1 клик за клик", "cost": 10, "cpc": 1, "weekly_bonus": 0, "image": "default.png"},
    "novikov": {"name": "Новиков", "description": "+70 кликов в секунду", "cost": 10000, "cps": 70, "weekly_bonus": 0, "image": "default.png"},
    "harach": {"name": "Харач", "description": "+2 клика в секунду и +10000 бонусов в неделю", "cost": 15000, "cps": 2, "weekly_bonus": 10000, "image": "default.png"},
    "volkov": {"name": "Волков", "description": "+5 кликов в секунду", "cost": 13500, "cps": 5, "weekly_bonus": 0, "image": "default.png"}
}

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
            db = init_connection()  # get new connection here!
            cursor = db.cursor()
            cursor.execute("UPDATE clicks SET count = ?, last_bonus_time = ? WHERE user_id = ?", (st.session_state.count, now, st.session_state.user_id))
            db.commit()

    else:
        bonus = 0
        for upgrade_name in upgrade_names:
            if st.session_state.upgrades[upgrade_name] == 1 and upgrades_info[upgrade_name].get('weekly_bonus'):
                bonus += upgrades_info[upgrade_name]['weekly_bonus']

        st.session_state.count += bonus
        st.session_state.last_bonus_time = now
        db = init_connection()   # Moved here
        cursor = db.cursor()
        cursor.execute("UPDATE clicks SET count = ?, last_bonus_time = ?  WHERE user_id = ?", (st.session_state.count, now, st.session_state.user_id))



        db.commit()



def update_count_with_cps():
    db = init_connection() # get db connection here
    cursor = db.cursor()



    try:


        cursor.execute(f"SELECT {', '.join(upgrade_names)} FROM clicks WHERE user_id = ?", (st.session_state.user_id,))

        result = cursor.fetchone()




        if result:
            cps = 0



            for i, upgrade_name in enumerate(upgrade_names):
                if result[i] == 1:


                  if 'cps' in upgrades_info[upgrade_name]:


                     cps += upgrades_info[upgrade_name]['cps']
            st.session_state.count += cps




            cursor.execute("UPDATE clicks SET count = ? WHERE user_id = ?", (st.session_state.count, st.session_state.user_id))

            db.commit()





            st.session_state.cps = cps



            return cps


    except Exception as e:

        print("ERROR applying update count with cps", e)




        return 0



def increment():
    db = init_connection()
    cursor = db.cursor()
    try:

        st.session_state.count += st.session_state.cpc
        cursor.execute("UPDATE clicks SET count = ? WHERE user_id = ?", (st.session_state.count, st.session_state.user_id,))
        db.commit()
    except Exception as e:
        print(e)

update_count_with_cps()

st.title("Simple Clicker")

st.write(f"Count: {st.session_state.count}")



st.button("Click me!", on_click=increment, type="primary")
st.write(f"Clicks per second: {st.session_state.cps}")


placeholder = st.empty()




i = 0
def auto_click():


    give_weekly_bonus()



    new_cps = update_count_with_cps()





    global i


    i += 1


    placeholder.text(f'{st.session_state.count}')
    time.sleep(1/new_cps if new_cps >0 else 1)





auto_click()


st.experimental_rerun()




st.title('Магазин')




for upgrade_name, upgrade in upgrades_info.items():



  if st.session_state.upgrades[upgrade_name] == 0:



        if st.button(f"Buy {upgrade['name']} for {upgrade['cost']}"):




           can_buy = st.session_state.count >= upgrade['cost']


           if can_buy:

            db = init_connection()

            cursor = db.cursor()

            st.session_state.upgrades[upgrade_name] = 1


            st.session_state.count -= upgrade['cost']




            cursor.execute("UPDATE clicks SET count = ?, {} = 1 WHERE user_id = ?".format(upgrade_name),(st.session_state.count,st.session_state.user_id))





            db.commit()

            st.session_state.cpc += upgrade.get('cpc', 0)



            update_count_with_cps()


            st.experimental_rerun()





           else:





              st.write("you cannot buy this yet.")



st.write("Your orioks now:"+str(st.session_state.count))

for upgrade in upgrade_names:
    if st.session_state['upgrades'][upgrade] == 1:


       st.write("Your purchased widget: " + upgrade)
