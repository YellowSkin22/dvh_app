# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:24:01 2022

@author: bruce
"""

### --- Libraries --- ### 
import streamlit as st
import pandas as pd
from datetime import date

### --- Relevant URLS --- ### 
# https://www.webfx.com/tools/emoji-cheat-sheet/
# https://raw.githubusercontent.com/YellowSkin22/dvh_app/main/data/bankrekening_2022.csv

### --- DataFrame Work --- ###
transactions_url = 'https://raw.githubusercontent.com/YellowSkin22/dvh_app/main/data/bankrekening_2022.csv'
transactions_df = pd.read_csv(transactions_url,
                              sep=',',
                              encoding='latin-1')

member_mutations_url = 'https://raw.githubusercontent.com/YellowSkin22/dvh_app/main/data/member_mutation_summary.csv'
member_mutations_df = pd.read_csv(member_mutations_url)
member_mutations_df['total'] = member_mutations_df.incoming - member_mutations_df.outgoing

## -- DataFrame CleanUp -- ##


### --- Metric Variables --- ###
## -- Member Count -- ##
original_membercount = 229
mutations = member_mutations_df['total'].sum()
current_membercount = original_membercount + mutations
last_member_date = member_mutations_df.date.iloc[-1]




## -- Bank Account Balance -- ##
account_balance = transactions_df['Saldo na trn'].iloc[-1]
account_balance = account_balance.replace('+', '')
account_balance = account_balance.replace(',', '.')
account_balance = float(account_balance)

last_account_date = transactions_df['Datum'].iloc[-1]

### --- Streamlit App --- ###

## -- Display -- ##
st.set_page_config(layout='wide') #Set app to widescreen

## -- Header -- ##
st.title(':baseball: DVH Board Report')

## -- KPI Metrics -- ##
col1, col2, col3 = st.columns([1,1,6])

with col1:
    st.metric(label='Member Count',
              value=current_membercount,
              delta=None,
              help='Last update: {}'.format(last_member_date))

with col2:
    st.metric(label='Bank Account Balance',
              value=account_balance,
              delta=None,
              help='Last update: {}'.format(last_account_date))



## -- Tabs -- ##
tab1, tab2, tab3 = st.tabs(['Member Count', 'Cashflow', 'TBD'])

with tab1:
    st.header(':couple: Member Progression')
    st.write(current_membercount)
    st.write(original_membercount)
    st.write(member_mutations_df)
    
with tab2:
    st.write(transactions_df)
    st.write(account_balance)
    
    
    



