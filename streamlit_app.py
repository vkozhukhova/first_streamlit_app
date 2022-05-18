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

def get_fruit_data(fruit_choice):
  fr_resp = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_choice)
  fr_resp_norm = pandas.json_normalize(fr_resp.json())
  return fr_resp_norm

streamlit.header('🍌🥭 Fruityvice Fruit Advice 🥝🍇')
try:
  fruit = streamlit.text_input('Select a fruit to get info about')
  if not fruit:
    streamlit.error("Please select a fruit!!!")
  else:
    fr_resp_norm = get_fruit_data(fruit)
    streamlit.dataframe(fr_resp_norm)
except URLError as e:
  streamlit.error()

#streamlit.stop()

streamlit.header("Fruit load list contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list())
  my_cnx.close()

def insert_row(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute(f"insert into fruit_load_list values (' {new_fruit} ')")
    return 'Thank for adding ' + new_fruit
  
fruit_add = streamlit.text_input('What fruit would you like to add', 'jackfruit')
if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  func_resp = insert_row(fruit_add)
  my_cnx.close()
  streamlit.text(func_resp)
