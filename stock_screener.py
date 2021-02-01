from numpy.core.fromnumeric import size
import streamlit as st
st.set_page_config(layout='wide')
import pandas as pd
import matplotlib.pyplot as plt
# import plotly.express as pe
import mplfinance as mpl
import yfinance as yf
st.set_option('deprecation.showPyplotGlobalUse', False)




# build app #
def main():

  
    ### sidebar ###

    st.sidebar.header('Chart Setup.')
    filter_period = st.sidebar.select_slider(
            'Time period:',
            value='6mo',
            options= ['1mo', '3mo', '6mo', '1y', '2y']
        )

    filter_interval = st.sidebar.selectbox(
            'Interval:',
            index=1,
            options=['1h', '1d', '1wk']
        )

    chart_type = st.sidebar.radio('Chart Type:',['Candle', 'OHLC', 'Line', 'PNF'])



    ### webpage ###

    st.title("Stock Screener")
    st.write('Select a strategy or lookup a specific stock')

    # st.markdown("#")

    # col01, col02, col03, col04, col05, col06 = st.beta_columns(6)
    # with col01:
    #     if st.button("Setting New Lows"):
    #         st.warning("Coming Soon!")  ## yahoo finance screeners

    # with col02:
    #     if st.button("Setting New Highs"):
    #         st.warning("Coming Soon!")
    # with col03:
    #     if st.button("Undervalued Stocks"):
    #         st.warning("Coming Soon!")
    # with col04:
    #     if st.button("High Dividends (>5%)"):
    #         st.warning("Coming Soon!")
    # with col05:
    #     if st.button("Most Active"):
    #         st.warning("Coming Soon!")
    # with col06:
    #     if st.button("Insider Trading"):
    #         st.warning("Coming Soon") ## openinsider insider purchases

    # st.markdown("___")


    col1, col2, col3, col04, col05, col06 = st.beta_columns([2,1,2,2,2,3])
    with col1:
        filter_stock = st.text_input(label="", value='AAPL')
    with col2:
        st.write("")
    with col3:
        if st.button("Setting New Lows"):
            st.warning("Coming Soon!")
        if st.button("Setting New Highs"):
            st.warning("Coming Soon!")
    with col04:
        if st.button("High Dividends (>5%)"):
            st.warning("Coming Soon!")
        if st.button("Undervalued Stocks"):
            st.warning("Coming Soon!")
    with col05:
        if st.button("Most Active"):
            st.warning("Coming Soon!")
        if st.button("Insider Trading"):
            st.warning("Coming Soon") ## openinsider insider purchases
    with col06:
        st.write("")



    with st.spinner("Wait for it....!"):
        if st.button('Get stock data'):
            chart_data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)
            stock_data = yf.Ticker(filter_stock.upper())

            st.header(f"{stock_data.info['shortName']} {stock_data.info['symbol']}")

            col7, col8, col9 = st.beta_columns(3)
            with col7:
                st.title('${:0,.2f}'.format(stock_data.info['ask']))
            with col9:
                st.write('52W High| ${:0,.2f}'.format(stock_data.info['fiftyTwoWeekHigh']))
                st.write('52W Low| ${:0,.2f}'.format(stock_data.info['fiftyTwoWeekLow']))

            with col8:
                close_prior = stock_data.info['previousClose']
                ask_current = stock_data.info['ask']
                chg_frm_close = ask_current - close_prior
                pct_chg_frm_close = chg_frm_close/close_prior
                chg_frm_close = "${:0,.2f}".format(chg_frm_close).replace('$-','-$')
                pct_chg_frm_close = "{:.1%}".format(pct_chg_frm_close).replace('$-','-$')

                st.header(f"{chg_frm_close}  ({pct_chg_frm_close})")
                st.write("Change from close")

            col10, col11, col12, col13, col14 = st.beta_columns([0.5,15,1,12,0.5])
            with col11:
                st.write(filter_stock.upper())
                stock_fig = mpl.plot(data=chart_data[filter_stock.upper()], type=chart_type.lower(), style='yahoo', mav=(5,10,25), volume=True)
                st.pyplot(stock_fig)
            with col13:
                st.write('Chart Data:')
                st.dataframe(chart_data[filter_stock.upper()], height=600)
                # st.write(chart_data[filter_stock.upper()])
            with col10, col12, col14:
                st.write("")

            st.markdown("##")
            st.markdown("___")
           
            st.text_area(label=f"About {stock_data.info['shortName']}", value=stock_data.info['longBusinessSummary'], height=200)


            with st.beta_expander(label='Expand for Insider Trading (SEC Form 4):'):
                url = (f'http://openinsider.com/screener?s={filter_stock}&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1')
                read_insider = pd.read_html(url)
                insider = read_insider[-3].iloc[:,1:11]
                st.write(insider)



if __name__=='__main__':
    main()

