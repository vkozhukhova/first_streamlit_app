import streamlit
import pandas

streamlit.title("My parents new healthy diner")

streamlit.header('🥣 Breakfast Menu')

streamlit.text('🥗 Omega 3 & Blueberry Oatmeal')
streamlit.text('🐔 Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')    

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

selected = streamlit.multiselect('Pick some fruits here:', list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[selected]

streamlit.dataframe(fruits_to_show)

streamlit.header('🍌🥭 Fruityvice Fruit Advice 🥝🍇')
import requests
fruit = streamlit.text_input('Select a fruit to get info about', 'kiwi')
streamlit.write('User entered ' + fruit)
fr_resp = requests.get("https://www.fruityvice.com/api/fruit/" + fruit)
fr_resp_norm = pandas.json_normalize(fr_resp.json())
streamlit.dataframe(fr_resp_norm)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
