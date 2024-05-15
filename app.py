import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#st.set_page_config(layout='centered',page_title='Startup Analysis')
st.set_page_config(layout='wide',page_title='Startup Analysis')




df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')

def load_investor_details(investor):
    st.title(investor)
    st.subheader('Most Recent Investments')
    recent_investment_df = df[df['investors'].str.contains(investor)].sort_values('date',ascending=False).head(5)[['date','startup','vertical','city','round','amount']]
    st.dataframe(recent_investment_df)

    col1,col2 = st.columns(2)

    with col1:



        st.subheader('Biggest Investment')
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()


        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        st.subheader('Sectors Invested in')
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending=False)
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index,autopct='%0.01f%%')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader('Stages Invested in')
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(
            ascending=False)
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)

    with col4:
        st.subheader('Cities Invested in')
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(
            ascending=False)
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    df['year'] = df['date'].dt.year
    st.subheader('Year on Year Investment')
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)
    st.pyplot(fig4)









st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis', 'StartUp', 'Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'StartUp':
    st.title('StartUp Analysis')
    st.sidebar.selectbox('Select One', sorted(df['startup'].unique()))
    bt1 = st.sidebar.button('Find StartUp Details')
else:
    selected_investor = st.sidebar.selectbox('Select One', sorted(set((df['investors'].str.split(',')).sum())))
    bt2 = st.sidebar.button('Find Investor Details')
    if bt2:
        load_investor_details(selected_investor)


