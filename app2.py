import streamlit as st
from openai import OpenAI
import time
import pandas as pd
# Function to process audio
import os
client = OpenAI()
openai_config = {"temperature": 1,
                "max_tokens": 256,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0}
prompt="""Given a user query, your role is to analyze and classify it into one of the following categories: Network & Wireless, Accessories, Access Requests, VPN access, Jira Requests, Data Center Services, Data Center Services /Report VM issue, Data Center Services /VM Request, Software Request, Email Services, Hardware, Hardware Issue, Network, Newhire Accounts, Password Reset, Software Installation & Configuration. Additionally, determine the sentiment of the query from the options: Very Positive, Positive, Neutral, Negative, Very Negative. Start by identifying keywords or phrases that suggest a category, then assess the tone to estimate the sentiment. After your analysis, format your response as JSON with the category and sentiment fields."
For example, if the user query is 'I need help setting up my VPN. It's quite urgent as I have a deadline approaching.', your analysis might go like this: The mention of 'VPN' suggests the 'VPN access' category. The urgency and deadline imply a stressed tone, which could be considered 'Negative'. Hence, your JSON response should be: {"category": "VPN access", "sentiment": "Negative"}"""
def exctractor(l):
   prompts = [
       {
           "role": "system",
           "content": prompt
       },
       {
           "role": "user",
           "content": str(l)
       }]
   t = time.time()
   response2 = client.chat.completions.create(
       model="gpt-4-0125-preview",
       messages=prompts,
       temperature=openai_config["temperature"],
       max_tokens=openai_config["max_tokens"],
       top_p=openai_config["top_p"],
       frequency_penalty=openai_config["frequency_penalty"],
       presence_penalty=openai_config["presence_penalty"]
       )
   return response2.choices[0].message.content

# Streamlit app enhancements for better UI
def ticket_category_app():
   st.title("CtrlS Ticketting Analyzer")
   # Enhanced user query input area
   user_input = st.text_area("Enter your query", height=150)
   # Display available categories in a cleaner format
   categories = [
       'Network & Wireless',
       'Accessories',
       'Access Requests',
       'VPN access',
       'Jira Requests',
       'Data Center Services',
       'Data Center Services /Report VM issue',
       'Data Center Services /VM Request',
       'Software Request',
       'Email Services',
       'Hardware',
       'Hardware Issue',
       'Network',
       'Newhire Accounts',
       'Password Reset',
       'Software Installation & Configuration'
   ]
   with st.expander("Click to see predefined ticketing categories"):
       st.write(", ".join(categories))
   if user_input:
       with st.spinner('Analyzing your query...'):
           ans = exctractor(user_input)
       ans_eval = eval(ans)  # Consider using a safer alternative for eval if possible
       # Use columns to display the output in a more structured way
       col1, col2 = st.columns(2)
       with col1:
           st.subheader("Identified Category:")
           st.success(ans_eval["category"])
       with col2:
           st.subheader("Identified Sentiment:")
           st.success(ans_eval["sentiment"])
if __name__ == "__main__":
   ticket_category_app()
