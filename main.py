# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 08:24:01 2022

@author: bruce
"""

### --- Libraries --- ### 
import streamlit as st
import pandas as pd
# from datetime import date
# import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
# import matplotlib as mpl

### --- Functions --- ### 

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True
    
    


if check_password():

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
    
    memberconversions_url = 'https://raw.githubusercontent.com/YellowSkin22/dvh_app/main/data/member_conversion.csv'
    memberconversions_df = pd.read_csv(memberconversions_url)
    
    
    
    ## -- DataFrame CleanUp -- ##
    transactions_df['Saldo na trn'] = transactions_df['Saldo na trn'].str.replace('+', '')
    transactions_df['Saldo na trn'] = transactions_df['Saldo na trn'].str.replace(',', '.')
    transactions_df['Saldo na trn'] = transactions_df['Saldo na trn'].astype(float)
    
    ### --- Metric Variables --- ###
    ## -- Member Count -- ##
    original_membercount = 222
    last_member_date = member_mutations_df.date.iloc[-1]
    
    member_mutations_df['mutations'] = member_mutations_df.incoming - member_mutations_df.outgoing
    member_mutations_df['cumulative'] = member_mutations_df.mutations.cumsum()
    member_mutations_df['balance'] = original_membercount + member_mutations_df.cumulative
    
    mutations_total = member_mutations_df['mutations'].sum()
    current_membercount = original_membercount + mutations_total
    
    memberchart_df = member_mutations_df[['date', 'balance']]
    memberchart_df['date'] = memberchart_df['date'].str[3:]
    
    ## -- Member Conversion -- ## 
    conversion_2021 = round((10/31) * 100, 2)
    conversion_2022 = round((memberconversions_df.membership_y.count() / memberconversions_df.age.count()) * 100 , 2)
    
    conversion_delta = conversion_2022 - conversion_2021
    
    
    
    ## -- Bank Account Balance -- ##
    account_balance = transactions_df['Saldo na trn'].iloc[-1]
    
    last_account_date = transactions_df['Datum'].iloc[-1]
    
    ## - Visualisations -- ##
    
    # - Font Sizes - #
    
    SMALL_SIZE = 8
    MEDIUM_SIZE = 12
    BIGGER_SIZE = 14 
    
    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    
    # - fig1: Member Line Chart - #
    
    x = memberchart_df.date
    y = memberchart_df.balance
    
    fig1, ax1 = plt.subplots(figsize=(14, 4), layout='constrained')
    
    ax1.plot(x, y, label='member count', marker='o')  # Plot some data on the axes.
    
    for x, y in zip(x, y):
        label = y
        plt.annotate(label, (x, y),
                     xycoords="data",
                     textcoords="offset points",
                     xytext=(0, 10), ha="center")
    
    ax1.set_ylabel('member count')  # Add a y-label to the axes.
    ax1.tick_params(rotation=30, axis='x')  # rotate xticks
    ax1.set_ylim([220, 250])
    
    buf1 = BytesIO()
    fig1.savefig(buf1, format="png")
    
    # - fig2: Cash Flow Chart - #
    
    cashflowchart_df = transactions_df.groupby('Datum', as_index=False)['Saldo na trn'].last()
    
    x = cashflowchart_df['Datum']
    y = cashflowchart_df['Saldo na trn']
    
    fig2, ax2 = plt.subplots(figsize=(14, 4), layout='constrained')
    
    ax2.plot(x, y, label='Cash flow')  # Plot some data on the axes.
    
    
    ax2.set_ylabel('Cash Flow')  # Add a y-label to the axes.
    ax2.tick_params(rotation=30, axis='x')  # rotate xticks
    
    buf2= BytesIO()
    fig2.savefig(buf2, format="png")
    
    
    
    
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
    tab1, tab2, tab3 = st.tabs(['Member Count', 'Cashflow', 'P&L'])
    
    with tab1:
        st.header(':couple: Member Progression')
        st.caption("""Voortgang op aantallen leden op basis van totalen. Conversion rate is op basis van leden die lid worden na een proeftraining.""")
        
        
        col1, col2 = st.columns([1,4])
        
        with col1:
            st.metric(label='Member Count',
                      value=current_membercount,
                      delta=None,
                      help='Last update: {}'.format(last_member_date))
            
            st.metric(label='Conversion Rate',
                      value='{} %'.format(conversion_2022),
                      delta=conversion_delta,
                      help='Last update: {}'.format('tbd'))
            
            st.metric(label='TBD',
                      value=0,
                      delta=-1,
                      help='Last update: {}'.format('tbd'))
        
        
        with col2:
            st.image(buf1)
        
        
    with tab2:
        st.image(buf2)
        
    
    



