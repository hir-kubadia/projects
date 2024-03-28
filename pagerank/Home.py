from streamlit_extras.app_logo import add_logo
from thefuzz import fuzz, process
import pandas as pd
import numpy as np
import networkx as nx
import streamlit as st
import re

add_logo(r"C:\Users\hirlk\Downloads\nmims_project\pagerank\H_Mart_logo.png")
st.title('Welcome to HMart!')

df = pd.read_csv('OnlineRetail.csv', encoding = 'unicode-escape')
df.dropna(inplace = True)
stock_info = df.groupby('Description').agg({'StockCode': 'first', 'UnitPrice': 'first', 'InvoiceNo': 'nunique'}).reset_index()

def stripper(df):
    desc = []
    for i in df['Description']:
        desc.append(i.strip())
    
    df['Description'] = desc
    return df

df = stripper(df)
stock_info = stripper(stock_info)

def anything(df):
    G = nx.from_pandas_edgelist(df, source='CustomerID', target='StockCode', create_using=nx.DiGraph())
    dict1 = df.groupby('Description')[['StockCode']].first().reset_index()
    dict1 = dict1.set_index('StockCode').to_dict()['Description']
    pagerank_scores = nx.pagerank(G)
    ranked_products = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
    ranked_products = [dict1.get(j) for i in ranked_products for j in i]
    return ranked_products

home_page_products = anything(df)

text = st.text_input('What would you like to purchase today...', value="")

# To do :- In the results first keep the one which exactly match and then the ones which fuzzily match

def search_result(df, text):
    results = []
    products = list(df['Description'].unique())
    for i in products:
        j_results = []
        for j in re.split('\s', text):
            if re.search(pattern = fr'.{j.lower()}.', string = str(i).lower()):
                j_results.append(i)
        if len(j_results) == len(re.split('\s', text)):
            results.append(i)
        elif fuzz.partial_ratio(text.lower(), str(i).lower()) >= 74:
            results.append(i)
    return results

N_cards_per_row = 3

if text:
    results = search_result(df, text)
    ranked_products = anything(df.loc[df['Description'].isin(results)])
    if len(ranked_products[::2]) > 0:
        for i,j in enumerate(ranked_products[::2]):
            index = i % N_cards_per_row
            if index == 0:
                st.write("---")
                cols = st.columns(N_cards_per_row, gap="large")
                # draw the card
            with cols[i % N_cards_per_row]:
                many = stock_info[stock_info['Description'] == j]['InvoiceNo'].iloc[0]
                st.markdown(f'This item was ordered **{many}** times.')
                st.write(f"**{j.strip()}**")
                st.caption(f"Stock Code: **{str(stock_info[stock_info['Description'] == j]['StockCode'].iloc[0]).strip()}** ")
                st.text(f"Price: {float(stock_info[stock_info['Description'] == j]['UnitPrice'])}$")
    else:
        st.write('Sorry, for now we\'re out of:', f'**{text}**')

    


















