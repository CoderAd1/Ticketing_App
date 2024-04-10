import streamlit as st

from openai import OpenAI

import pandas as pd

import os

# Initialize OpenAI client

client = OpenAI()

# Configuration for OpenAI API

openai_config = {

    "temperature": 1,

    "max_tokens": 256,

    "top_p": 1,

    "frequency_penalty": 0,

    "presence_penalty": 0

}

# The prompt to guide the model's response

prompt=""""Given a user query, your role is to analyze and classify it into one of the following categories: Network & Wireless, Accessories, Access Requests, VPN access, Jira Requests, Data Center Services, Data Center Services /Report VM issue, Data Center Services /VM Request, Software Request, Email Services, Hardware, Hardware Issue, Network, Newhire Accounts, Password Reset, Software Installation & Configuration. Additionally, determine the sentiment of the query from the options: Very Positive, Positive, Neutral, Negative, Very Negative. Start by identifying keywords or phrases that suggest a category, then assess the tone to estimate the sentiment. Subsequently, provide a deep analysis of the query with a step-by-step solution to the problem, ensuring your tone of voice is professional. After your analysis, format your response as JSON with the category, sentiment, and solution fields."
 You should strictly  only give a json as the output in the specified format.
For example, if the user query is 'I need help setting up my VPN. It's quite urgent as I have a deadline approaching.', your analysis might go like this: The mention of 'VPN' suggests the 'VPN access' category. The urgency and deadline imply a stressed tone, which could be considered 'Negative'. A professional, step-by-step solution could involve verifying network connections, ensuring VPN software is up to date, and contacting IT support if issues persist. Hence, your JSON response should be: {"category": "VPN access", "sentiment": "Negative", "solution": "1. Verify your network connection. 2. Ensure your VPN software is updated. 3. Restart your VPN service. 4. If the problem persists, contact IT support for further assistance."}
"""

def extractor(query):

    prompts = [

        {"role": "system", "content": prompt},

        {"role": "user", "content": str(query)}

    ]

    response = client.chat.completions.create(

        model="gpt-4-0125-preview",

        messages=prompts,

        temperature=openai_config["temperature"],

        max_tokens=openai_config["max_tokens"],

        top_p=openai_config["top_p"],

        frequency_penalty=openai_config["frequency_penalty"],

        presence_penalty=openai_config["presence_penalty"]

    )

    return response.choices[0].message.content

def analyze_and_display_queries(queries):

    results = []

    for query in queries:

        ans = extractor(query)

        ans_eval = eval(ans)  # Consider using a safer alternative for eval if possible

        results.append([query, ans_eval["category"], ans_eval["sentiment"]])

    # Convert results to DataFrame for sorting and display

    df = pd.DataFrame(results, columns=["Description", "Category", "Sentiment"])

    df["Sentiment Rank"] = df["Sentiment"].map({"Very Negative": 0, "Negative": 1, "Neutral": 2, "Positive": 3, "Very Positive": 4})

    df.sort_values("Sentiment Rank", inplace=True)

    df.drop("Sentiment Rank", axis=1, inplace=True)

    st.table(df)

# Streamlit app with tabs

def ticket_category_app():

    tab1, tab2 = st.tabs(["Single Query", "Bulk Query"])

    # Single Query Tab

    with tab1:

        st.title("CtrlS Ticketting Analyzer - Single Query")

        user_input = st.text_area("Enter your query", height=150)

        if user_input:

            with st.spinner('Analyzing your query...'):

                ans = extractor(user_input)

            ans_eval = eval(ans)  # Consider safer alternatives

            # Display Category and Sentiment

            st.subheader("Identified Category:")

            st.success(ans_eval["category"])

            st.subheader("Identified Sentiment:")

            st.success(ans_eval["sentiment"])

            # Display Solution in a wider, colored block
            st.subheader("Identified Solution:")
            st.markdown("""<style>.solutionBox { background-color: #173928; padding: 10px; border-radius: 10px; }</style>""", unsafe_allow_html=True)

            st.markdown(f"<div class='solutionBox'><h3 style='color: #333;'></h3><p>{ans_eval['solution']}</p></div>", unsafe_allow_html=True)

    # Bulk Query Tab

    with tab2:

        st.title("CtrlS Ticketting Analyzer - Bulk Query")

        query_count = st.number_input('How many queries would you like to analyze?', min_value=1, value=1, step=1)

        queries = [st.text_area(f"Query-{i+1}", key=f"query-{i}") for i in range(query_count)]

        analyze_button = st.button("Analyze Queries")

        if analyze_button:

            analyze_and_display_queries(queries)

if __name__ == "__main__":

    ticket_category_app()
