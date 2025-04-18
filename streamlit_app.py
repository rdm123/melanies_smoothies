# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothie! """
)

# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Banana", "Strawberries", "Peaches"),
# )
name_on_order=st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)
# title=st.text_input('Movie title','Life of Brian')
# st.write('The current movie title is',title)
# st.write("You selected:", option)
cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('Choose up to 5 ingredients:',my_dataframe, max_selections=5)
if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)
   ingredients_string=''
   for fruit_chosen in ingredients_list:
       ingredients_string+=fruit_chosen+' '
       
   st.write(ingredients_string)  
   my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

   st.write(my_insert_stmt)
   time_to_insert=st.button('Submit Order') 
   if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
 
#Replace the code in this example app with your own code! And if you're new to Streamlit, here are some helpful links:  • :page_with_curl: [Streamlit open source documentation]({helpful_links[0]})
#     • :snow: [Streamlit in Snowflake documentation]({helpful_links[1]}) 
#     • :books: [Demo repo with templates]({helpful_links[2]})
#     • :memo: [Streamlit in Snowflake release notes]({helpful_links[3]})
# # Get the current credentials
# session = get_active_session()

# # Use an interactive slider to get user input
# hifives_val = st.slider(
#     "Number of high-fives in Q3",
#     min_value=0,
#     max_value=90,
#     value=60,
#     help="Use this to enter the number of high-fives you gave in Q3",
# )

# #  Create an example dataframe
# #  Note: this is just some dummy data, but you can easily connect to your Snowflake data
# #  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
# created_dataframe = session.create_dataframe(
#     [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
#     schema=["HIGH_FIVES", "FIST_BUMPS", "QUARTER"],
# )

# # Execute the query and convert it into a Pandas dataframe
# queried_data = created_dataframe.to_pandas()

# # Create a simple bar chart
# # See docs.streamlit.io for more types of charts
# st.subheader("Number of high-fives")
# st.bar_chart(data=queried_data, x="QUARTER", y="HIGH_FIVES")

# st.subheader("Underlying data")
# st.dataframe(queried_data, use_container_width=True)
