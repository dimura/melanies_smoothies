# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothie:cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your smoothie.
  """
)

name_on_order = st.text_input('Name on smoothie:')

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
df = my_dataframe.to_pandas()
ingredients_list = st.multiselect('Choose up to 5', my_dataframe,  max_selections=5)

if ingredients_list:

    ingredients_string = ''
    for i in ingredients_list:
        ingredients_string+=i + ' '
        st.subheader(i + ' Nutrition Information')
        search_value = df.loc[df['FRUIT_NAME'] == i, 'SEARCH_ON'].values[0]
        if search_value is None: search_value=i
        st.write(search_value)
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_value}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """' )"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}', icon="✅")

#st.write(my_insert_stmt)
