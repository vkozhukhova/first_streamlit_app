import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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
try:
  fruit = streamlit.text_input('Select a fruit to get info about')
  if not fruit:
    streamlit.error("Please select a fruit!!!")
  else:
    fr_resp = requests.get("https://www.fruityvice.com/api/fruit/" + fruit)
    fr_resp_norm = pandas.json_normalize(fr_resp.json())
    streamlit.dataframe(fr_resp_norm)
except URLError as e:
  streamlit.error()

streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("Fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_add = streamlit.text_input('What fruit would you like to add', 'jackfruit')
streamlit.write('User added ' + fruit_add)
my_cur.execute("insert into fruit_load_list values ('')")
