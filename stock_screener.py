import streamlit as st
st.set_page_config(layout='centered')
import pandas as pd

import matplotlib.pyplot as plt
import mplfinance as mpl

import yfinance as yf


# build app #
def main():

    # webpage #

    st.title("Stock Screener")

    @st.cache()
    def load_data():
        data=yf.download(['SPY', 'NDAQ', 'DJIA'], period='3mo', interval='1d', group_by='ticker')

        return data
    
    data=load_data()
    
    # col1, col2, col3 = st.beta_columns(3)
    # with col1:
    #     # spy_data=yf.download('SPY', period='6mo', interval='1d', group_by='ticker', auto_adjust=True)
    #     sp_plot= mpl.plot(data['SPY'], type='line', style='mike', volume=True,  title='S&P500')
    #     st.pyplot(fig=sp_plot)
    # with col2:
    #     # ndaq_data=yf.download('NDAQ', period='6mo', interval='1d', group_by='ticker', auto_adjust=True)
    #     ndaq_plot= mpl.plot(data['NDAQ'], type='line', style='mike', volume=True,  title='NASDAQ')
    #     st.pyplot(fig=ndaq_plot)
    # with col3:
    #     # dow_data=yf.download('DJIA', period='6mo', interval='1d', group_by='ticker', auto_adjust=True)
    #     dow_plot= mpl.plot(data['DJIA'], type='line', style='mike', volume=True,  title='DOW')
    #     st.pyplot(fig=dow_plot)


    st.header('Stock Search')
    
    
    filter_period = '6mo'
    filter_interval = '1d'
    filter_movavg = False
    filter_volume = False


    col1, col2, col3, col4 = st.beta_columns(4)
    with col1:
        filter_stock = st.text_input(
        label='Insert ticker symbol.')
        
    with col2:
        chart_type = st.radio('Chart Type:',['line', 'candle', 'pnf'])
        
    with col3:
        filter_period = st.selectbox(
            'Time period:',
            key='6mo',
            options= ['1mo', '3mo', '6mo', '1y', '2y']
        )
    with col4:
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
        data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)



        st.markdown("#")

        stock_plot= mpl.plot(data=data[filter_stock.upper()], type=chart_type, style='charles', mav=(5,20,50), volume=True,  title=filter_stock.upper())
        
        st.pyplot(fig=stock_plot)

        with st.beta_expander(label='Click for data'):
            st.write(data[filter_stock.upper()])



   



if __name__=='__main__':
    main()