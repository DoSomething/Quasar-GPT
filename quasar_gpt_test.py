# Importing required packages
import streamlit as st
import openai
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(st.secrets["quasar_readonly_connection_string"])

st.title("Quasar GPT")
st.sidebar.header("Instructions")
st.sidebar.info(
    '''This is a web application that allows you to interact with 
       our quasar data warehouse using natural language.
       Enter a **query** in the **text box** and **click Send** to receive 
       a **response**.
       Note: **This is an experiment, this data is not necessarily correct** 😅 Also, errors have not yet been handled, so please refresh if you get an error message.
       '''
    )

openai.api_key = st.secrets["openai_api_key"]

with open('quasar_gpt_test_system_prompt.txt', 'r') as file:
	system_prompt = file.read()

def get_data(sql_query):
	return pd.read_sql_query(sql_query, engine)

def ChatGPT(user_query):
	completion = openai.ChatCompletion.create(
	  model="gpt-4",
	  messages=[
	  	 {"role": "system", "content": system_prompt},
	    {"role": "user", "content": user_query}
	  ]
	)

	return completion.choices[0].message

def submit():
	if user_query != "":
		# Pass the query to the ChatGPT function
		with st.spinner(text="Processing..."):
			query_to_send = str(user_query)
			if try_to_plot:
				query_to_send = query_to_send + " - the resulting table should have two columns, 'x' and 'y', so that I can plot this as a line chart"
			response = ChatGPT(query_to_send).content
			sql_query = response
			if '```sql' in sql_query:
				sql_query = sql_query[sql_query.find('```sql') + len('```sql'):sql_query.rfind('```')]
			st.code(sql_query, language='sql')
			df_to_display = get_data(response)
		st.success("Done!")
		if 'x' in df_to_display and 'y' in df_to_display:
			st.line_chart(data=df_to_display, x='x',y='y')
		return st.dataframe(df_to_display)

	else:
		st.write("Please enter a question.")

user_query = st.text_input("Enter query here", "")
try_to_plot = st.checkbox('Try to Plot?')
st.button('Send',on_click=submit)
