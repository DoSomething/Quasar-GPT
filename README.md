# Quasar-GPT
*Testing a new way to interact with our Data*

How it works:

- User enters a data-related question

- That question is sent to OpenAI along with a system prompt that defines our intention/schema

- OpenAI returns SQL query

- That SQL query is passed off to our warehouse

- The corresponding dataframe is displayed (and plot if 'Try to Plot?' is enabled)
