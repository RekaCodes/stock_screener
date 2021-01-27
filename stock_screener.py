import streamlit as st
st.set_page_config(layout='centered')
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpl
import yfinance as yf




# build app #
def main():

    st.title("Stock Screener")

    filter_period = '6mo'
    filter_interval = '1d'

    col1, col2, col3 = st.beta_columns([3,2,5])
    with col1:
        st.markdown("####")
        st.subheader("Insert ticker symbol:")
    with col2:
        filter_stock = st.text_input(label="", value='AAPL')
    with col3:
        st.write("")
    

    
    col3, col4, col5 = st.beta_columns([2,1,1])
    with col3:
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        chart_type = st.radio('Chart Type:',['Candle', 'OHLC', 'Line', 'PNF'])

    with col4:
        st.markdown("####")
        filter_period = st.selectbox(
            'Time period:',
            key='6mo',
            options= ['1mo', '3mo', '6mo', '1y', '2y']
        )

    with col5:
        st.markdown("####")
        filter_interval = st.select_slider(
            'Interval:',
            key='1d',
            options=['1h', '1d', '1wk']
        )

    if st.button('Get stock data'):
        data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)

        st.markdown("#")

        stock_plot= mpl.plot(data=data[filter_stock.upper()], type=chart_type.lower(), style='yahoo', mav=(5,10,25), volume=True,  title=filter_stock.upper())
        
        st.pyplot(fig=stock_plot)

        with st.beta_expander(label='Click for data'):
            st.write(data[filter_stock.upper()])


if __name__=='__main__':
    main()

