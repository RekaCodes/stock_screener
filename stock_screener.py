import streamlit as st

import pandas as pd
import pandas_datareader as pdr
import numpy as np

import matplotlib.pyplot as plt
import mplfinance as mpl

import yfinance as yf
st.set_option('deprecation.showPyplotGlobalUse', False)
# from stock_data import fig_stock


# build app #
def main():

    # webpage #

    st.title("Stock Screener")


    filter_stock = st.text_input(
        label='insert ticker symbol here')
    
    filter_period = '6mo'
    filter_interval = '1d'
    filter_movavg = False
    filter_volume = False


    col1, col2 = st.beta_columns(2)
    with col1:
        filter_period = st.selectbox(
            'Time period:',
            key='6mo',
            options= ['1mo', '3mo', '6mo', '1y', '2y']
        )
    with col2:
        filter_interval = st.select_slider(
            'Interval:',
            key='1d',
            options=['1h', '1d', '1wk']
        )
    
    # col3, col4 = st.beta_columns(2)
    # with col3:
        # check_avg = st.checkbox('Moving Average:')
        # if check_avg:
        #     filter_movavg == True
        # check_vol = st.checkbox('Volume')
        # if check_vol:
        #     filter_volume == 1


    
    if st.button('Get stock data'):
        data=yf.download([filter_stock, 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)



        st.markdown("#")

        fig1= mpl.plot(data=data[filter_stock], type='candle', mav=(5,20,50), volume=True,  title=filter_stock)
        
        st.pyplot(fig=fig1)

        with st.beta_expander(label='Click for data'):
            st.write(data[filter_stock])



   



if __name__=='__main__':
    main()