import streamlit as st

# Function to convert text to PDF
from openai import OpenAI
import time
import os

# Function to process audio
client = OpenAI()
openai_config={"temperature":0.3,
               "max_tokens":256,
               "top_p":1,
               "frequency_penalty":0,
               "presence_penalty":0}
prompt="""Given a user query, your role is to analyze and classify it into one of the following categories: Network & Wireless, Accessories, Access Requests, VPN access, Jira Requests, Data Center Services, Data Center Services /Report VM issue, Data Center Services /VM Request, Software Request, Email Services, Hardware, Hardware Issue, Network, Newhire Accounts, Password Reset, Software Installation & Configuration. Additionally, determine the sentiment of the query from the options: Very Positive, Positive, Neutral, Negative, Very Negative. Start by identifying keywords or phrases that suggest a category, then assess the tone to estimate the sentiment. After your analysis, format your response as JSON with the category and sentiment fields."
For example, if the user query is 'I need help setting up my VPN. It's quite urgent as I have a deadline approaching.', your analysis might go like this: The mention of 'VPN' suggests the 'VPN access' category. The urgency and deadline imply a stressed tone, which could be considered 'Negative'. Hence, your JSON response should be: {"category": "VPN access", "sentiment": "Negative"}"""
def exctractor(l):
    prompts=[
        {
        "role": "system",
        "content": prompt
        },
        {
        "role": "user",
        "content": str(l)
        }]
    t=time.time()
    response2 = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=prompts,
        temperature=openai_config["temperature"],
        max_tokens=openai_config["max_tokens"],
        top_p=openai_config["top_p"],
        frequency_penalty=openai_config["frequency_penalty"],
        presence_penalty=openai_config["presence_penalty"]
        )
    #print(time.time()-t)
    return response2.choices[0].message.content


# Streamlit app
import streamlit as st

def ticket_category_app():
    st.title("CtrlS Ticketting Analyzer ")
    
    # Text input for user's ticket description
    user_input = st.text_input("Enter your query", "")
    
    # Available categories
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
    
    # Display available categories
    st.write("Pre Defined Ticketing Categories:"+str(categories).replace("[","").replace("]",""))
    
    # Dummy processing (can be replaced with actual ticket categorization logic)
    if user_input:
        st.write("\nYour ticket description:")
        st.write(user_input)
        ans=exctractor(user_input)
        st.write("\nBased on the provided categories, a suitable category for your ticket could be:")
        st.write("\nThe identified category is:",eval(ans)["category"])
        st.write("\nThe identified sentiment is:",eval(ans)["sentiment"])

if __name__ == "__main__":
    ticket_category_app()

