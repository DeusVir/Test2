import streamlit as st
import time
import random
import secrets
import datetime
import sqlite3

DATABASE = 'clicker_data.db'  # Имя файла базы данных

# Функция для подключения к базе данных
def get_db():
    db = getattr(st.session_state, '_database', None)
    if db is None:
        db = st.session_state._database = sqlite3.connect(DATABASE)
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

@st.cache_resource  # Кешируем соединение с БД
def init_connection():
    return get_db()


db = init_connection() #initialize on startup

# Функция для получения данных из базы данных
def get_user_data(user_id):

    cursor = db.cursor()

    cursor.execute("SELECT count, last_bonus_time, fedorov_ml, fedorov_str, korneeva, epihin, zharkova, sokolova, kozhukhov, novikov, harach, volkov FROM clicks WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()



    if result:

        return result


    else:




        cursor.execute("INSERT INTO clicks (user_id) VALUES (?)", (user_id,))




        db.commit()

        return (0, None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)



# Инициализация состояния с данными из БД
if 'user_id' not in st.session_state:
    st.session_state.user_id = secrets.token_hex(8)


user_data = get_user_data(st.session_state.user_id)



if 'count' not in st.session_state:


    st.session_state.count = user_data[0]


if 'last_bonus_time' not in st.session_state:


  st.session_state.last_bonus_time = user_data[1]



if 'upgrades' not in st.session_state:

   upgrades = {}

   for index,upgrade_name in  enumerate(upgrade_names):

      upgrades[upgrade_name] = user_data[2+index] # slice starting from 2 for upgrades





   st.session_state.upgrades = upgrades
if 'cps' not in st.session_state:
    st.session_state.cps = 0
if 'cpc' not in st.session_state:
    st.session_state.cpc = 1



# Upgrades info (без изменений)




upgrade_names = list(upgrades_info.keys())


def give_weekly_bonus():
 # ... (без изменений)
                if bonus > 0:

                    cursor = db.cursor() #Get the database cursor

                    cursor.execute("UPDATE clicks SET count = count + ?, last_bonus_time = ? WHERE user_id = ?", (bonus, now, st.session_state.user_id))

                    db.commit()


        else: # ..(без изменений)





            if bonus > 0:
             cursor = db.cursor()



             cursor.execute("UPDATE clicks SET count = count + ?, last_bonus_time = ? WHERE user_id = ?", (bonus, now, st.session_state.user_id))




             db.commit()



#update_count_with_cps(db.cursor())

def update_count_with_cps():


    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT {', '.join(upgrade_names)} FROM clicks WHERE user_id = ?", (st.session_state.user_id,))

        result = cursor.fetchone()
        if result:

            cps = 0

            for i, upgrade_name in enumerate(upgrade_names):



                 if result[i] == 1:
                      if upgrades_info[upgrade_name].get('cps'):


                           cps += upgrades_info[upgrade_name].get('cps', 0)


            st.session_state.cps = cps




            cursor.execute("UPDATE clicks SET count = count + ? WHERE user_id = ?", (cps, st.session_state.user_id))


            db.commit() #Commit database changes





            st.session_state.count = st.session_state.count+ cps



            return cps

    except Exception as e:


        print("ERROR applying update count with cps", e)
        return 0

def increment():
 #Increment count in database and then update state




    try:




     cursor = db.cursor()




     cursor.execute("UPDATE clicks SET count = count + ? WHERE user_id = ?", (st.session_state.cpc, st.session_state.user_id,))

     db.commit() # Very important - commits database queries made so far




     st.session_state.count +=st.session_state.cpc

    except Exception as e:



       print(e)






# Отображение счетчика


st.title("Simple Clicker")


st.write(f"Count: {st.session_state.count}")




# Кнопка клика



st.button("Click me!", on_click=increment, type="primary") #Change appearance



st.write(f"Clicks per second: {st.session_state.cps}")




placeholder = st.empty()






#Autoclick




i = 0





def auto_click():

 give_weekly_bonus()





 new_cps = update_count_with_cps()
 time.sleep(1/new_cps) if new_cps > 0 else time.sleep(1)






 global i

 i+=1
 placeholder.text(f'{st.session_state.count}')



 #st.write("Now your clicksPerSecond are = "+ str(new_cps))




 time.sleep(1)







auto_click() # run once to give initial clicks




st.experimental_rerun()
