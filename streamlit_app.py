# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie!:cup_with_straw:")
st.write(
    """Select your fruit
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('Name on the Smoothie will be: ', name_on_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe
)
if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string +"""','"""+ name_on_order + """')"""

#st.write(my_insert_stmt)
#st.stop()
    
    time_to_insert =st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order+'!', icon="✅")
