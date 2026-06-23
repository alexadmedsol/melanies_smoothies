# Import python packages
import streamlit as st
import os
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Enter your name, then choose the fruits you want in your custom Smoothie!
  """
)

order_name = st.text_input(
    'Enter your name: '
    ,placeholder = 'John Smiith'
    ,max_chars=100)
if order_name:
    st.write('The name on your smoothie order will be ', order_name,'.')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    , max_selections = 5
    , placeholder='Choose ingredients...'
)
if ingredients_list and order_name:

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """', '"""+order_name+ """')"""
    
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered '+ order_name + '!', icon="✅")
else:
    st.write(':warning: Order incomplete!')

url = "https://my.smoothiefroot.com/api/fruit/watermelon"
smoothiefroot_response = requests.get(url)
# st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
