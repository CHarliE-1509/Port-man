import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf 
import plotly.express as px
import datetime as dt
import math
import base64


# Making Main Tabs
Home, Dashboard, Portfolio, Team = st.tabs(['Home', 'Dashboard', 'Portfolio', 'Team'])

#making of Home
with Home:

    def set_background(png_file):
        with open(png_file, "rb") as f:
            img_data = f.read()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{base64.b64encode(img_data).decode()});
                background-size: cover;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    set_background("image.jpg")
   # st.title('Welcome to Port-Man')
    st.image('Port-man Research_transparent.png')
        

#Making of Dashboard 
with Dashboard:
    st.title("Stock Dashboard")
    ticker='Reliance'
    start_date=dt.datetime(2020,1,1)
    end_date=dt.datetime.now()
    ticker=st.sidebar.text_input('Ticker', value='Reliance')
    start_date=st.sidebar.date_input('Start Date',value=dt.datetime(2020,1,1))
    end_date=st.sidebar.date_input('End Date',value=dt.datetime.now())

    ticker_data=yf.download(ticker+'.NS',start=start_date,end=end_date)
    fig = px.line(ticker_data,x=ticker_data.index, y=ticker_data['Adj Close'], title=ticker)
    st.plotly_chart(fig)

    # Making Tabs
    Stock_price, Financials, stock_news, technical_analysis = st.tabs(['Historical Price', 'Fundamentals', 'Stock News', 'Technicals'])

    with Stock_price:
        st.header(ticker+' Price')
        stock_data=ticker_data
        stock_data['Daily Return'] =stock_data['Adj Close']/stock_data['Adj Close'].shift(1) -1
        stock_data.dropna(inplace=True)
        st.write(stock_data)
        annual_return=stock_data['Daily Return'].mean()*252*100
        st.write(f'Annual Return of {ticker} is {annual_return} %')
        annual_std=np.std(stock_data['Daily Return']) *np.sqrt(252)*100
        st.write(f'Risk on {ticker} is {annual_std} %')

    from stocknews import StockNews
    with stock_news:
        st.header('Top News')
        sn= StockNews(ticker, save_news=False)
        df_news=sn.read_rss()
        for i in range(10):
            st.subheader(f'News {i+1}')
            st.write(df_news['published'][i])
            st.write(df_news['title'][i])
            st.write(df_news['summary'][i])
            title_sentiment=df_news['sentiment_title'][i]
            st.write(f'Title Sentiment : {title_sentiment}')
            news_sentiment=df_news['sentiment_summary'][i]
            st.write(f'News sentiment : {news_sentiment}')
        

    import pandas_ta as ta
    with technical_analysis:
        st.subheader(f'{ticker} Technicals')
        df=pd.DataFrame()
        indicator_list=df.ta.indicators(as_list=True)
        technical_ind=st.selectbox('Technical Indicators',options=indicator_list)
        method=technical_ind
        indicator=pd.DataFrame(getattr(ta,method)(low=ticker_data['Low'],close=ticker_data['Close'],high=ticker_data['High'],open=ticker_data['Open'],volume=ticker_data['Volume']))
        indicator['Close']=ticker_data['Close']
        fig_ind_new=px.line(indicator)
        st.plotly_chart(fig_ind_new)

