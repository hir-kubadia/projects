from streamlit_extras.app_logo import add_logo
import streamlit as st
import networkx as nx
import pandas as pd
import time

add_logo(r"C:\Users\hirlk\Downloads\nmims_project\pagerank\H_Mart_logo.png")
st.title('Hello World!')

df = pd.read_csv(r'C:\Users\hirlk\Downloads\nmims_project\pagerank\OnlineRetail.csv', encoding = 'unicode-escape')
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

home_page_products = anything(df)[::2][:9]

N_cards_per_row = 2
num_results = len(home_page_products)
num_slides = num_results // N_cards_per_row + 1

print(home_page_products)

for i,j in enumerate(home_page_products):
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
        time.sleep(2)




