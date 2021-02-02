from numpy.core.fromnumeric import size
import streamlit as st
st.set_page_config(layout='wide')
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpl
import yfinance as yf
st.set_option('deprecation.showPyplotGlobalUse', False)




# build app #
def main():

  
    ## Stock Selector ##

    st.sidebar.title('Stock Analysis')
    st.sidebar.write("Insert ticker or select strategy.")  
    st.sidebar.write("####") 
    

    filter_stock = st.sidebar.text_input(label="Insert Ticker Symbol", value='')
    
    chart_type = st.sidebar.radio('Chart Type:',['Candle', 'OHLC', 'Line', 'PNF'])
    
    filter_time_frame = st.sidebar.selectbox(
        "Time Frame",
        ['1D:5m', '5D:1h', '1Mo:1d', '3Mo:1d', '6Mo:1d', '1Y:1w', '2Y:1w'],
        index=4
    )

    filter_period = filter_time_frame[:3].lower()
    filter_interval = filter_time_frame[-2:].lower()
    

    if st.sidebar.button('Get stock data'):
        if filter_stock=="":
            st.warning("Don't forget to enter a ticker symbol.")
        else:
            with st.spinner("Wait for it....!"):
                # if st.button('Get stock data'):
                    chart_data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)
                    stock_data = yf.Ticker(filter_stock.upper())
                    try:                    
                        st.header(f"{stock_data.info['shortName']} {stock_data.info['symbol']}")
                    except HTTPError:
                        st.write('You forgot to enter a ticker!')



                    st.text_area(label=f"About {stock_data.info['shortName']}", value=stock_data.info['longBusinessSummary'], height=125)

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


                    stock_fig = plt.figure(figsize=(16,7))
                    ax = stock_fig.add_subplot(111)
                    mpl.plot(data=chart_data[filter_stock.upper()], type=chart_type.lower(), style='yahoo', mav=(5,10,25), ax=ax)
                    
                    from matplotlib.offsetbox import AnchoredText
                    at = AnchoredText(
                        f"{filter_stock.upper()}",
                        loc='upper left',
                        frameon=False,
                        prop=dict(fontsize=32, fontweight='bold', alpha=0.2))
                    ax.add_artist(at)
                    st.pyplot(stock_fig)
                    
                    
                    st.markdown("___")
                    
                    # st.write(stock_data.info) << keep for future features

                    with st.beta_expander(label="Expand for Chart Data:"):
                        st.dataframe(chart_data[filter_stock.upper()])

                    st.markdown("###")

                    with st.beta_expander(label='Expand for Insider Trading (SEC Form 4):'):
                        url = (f'http://openinsider.com/screener?s={filter_stock}&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1')
                        read_insider = pd.read_html(url)
                        insider = read_insider[-3].iloc[:,1:11]
                        st.write(insider)


    st.sidebar.write("___")


    ## Screener ##

    slct_screener = st.sidebar.selectbox(
    label='Select a Screening Strategy',
    options=['New Highs', 'New Lows', 'High Dividend Yield', 'Most Active', 'Undervalued', 'Insider Trading'],
    index=0
    )

    if st.sidebar.button("Run Screening Strategy"):
        st.warning(f"You chose the {slct_screener} strategy. Strategies will be implemented soon! For now select a stock.")

                

    

    
    
    
    
    
    
    
    
    
    
    
    # st.sidebar.header('Chart Setup.')
    # filter_period = st.sidebar.select_slider(
    #         'Time period:',
    #         value='6mo',
    #         options= ['1mo', '3mo', '6mo', '1y', '2y']
    #     )

    # filter_interval = st.sidebar.selectbox(
    #         'Interval:',
    #         index=1,
    #         options=['1h', '1d', '1wk']
    #     )

    # chart_type = st.sidebar.radio('Chart Type:',['Candle', 'OHLC', 'Line', 'PNF'])




#     col1, col2, col3, col04, col05, col06 = st.beta_columns([2,1,2,2,2,3])
#     with col1:
#         # filter_stock = st.text_input(label="", value='AAPL')
#     with col2:
#         st.write("")
#     with col3:
#         if st.button("Setting New Lows"):
#             st.warning("Coming Soon!")
#         if st.button("Setting New Highs"):
#             read_new_highs = pd.read_html('https://finviz.com/screener.ashx?v=111&f=exch_nyse,idx_sp500,ta_highlow52w_b0to5h&o=-volume&ar=180')
#             stocks_new_highs = read_new_highs[1]
#             st.write(stocks_new_highs)
#     with col04:
#         if st.button("High Dividends"):
#                 read_high_div = pd.read_html('https://finance.yahoo.com/screener/unsaved/7ab48c3d-8a8d-4e20-9e25-15138880c20c?dependentField=sector&dependentValues=')
#                 high_div = read_high_div[0]
#                 st.write(high_div)
#         if st.button("Undervalued Stocks"):
#             st.warning("Coming Soon!")
#     with col05:
#         if st.button("Most Active"):
#             st.warning("Coming Soon!")
#         if st.button("Insider Trading"):
#             st.warning("Coming Soon") ## openinsider insider purchases
#     with col06:
#         st.write("")

# # /html/body/table[3]/tbody/comment()


    # with st.spinner("Wait for it....!"):
    #     # if st.button('Get stock data'):
    #         chart_data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)
    #         stock_data = yf.Ticker(filter_stock.upper())

    #         st.header(f"{stock_data.info['shortName']} {stock_data.info['symbol']}")

    #         col7, col8, col9 = st.beta_columns(3)
    #         with col7:
    #             st.title('${:0,.2f}'.format(stock_data.info['ask']))
    #         with col9:
    #             st.write('52W High| ${:0,.2f}'.format(stock_data.info['fiftyTwoWeekHigh']))
    #             st.write('52W Low| ${:0,.2f}'.format(stock_data.info['fiftyTwoWeekLow']))

    #         with col8:
    #             close_prior = stock_data.info['previousClose']
    #             ask_current = stock_data.info['ask']
    #             chg_frm_close = ask_current - close_prior
    #             pct_chg_frm_close = chg_frm_close/close_prior
    #             chg_frm_close = "${:0,.2f}".format(chg_frm_close).replace('$-','-$')
    #             pct_chg_frm_close = "{:.1%}".format(pct_chg_frm_close).replace('$-','-$')

    #             st.header(f"{chg_frm_close}  ({pct_chg_frm_close})")
    #             st.write("Change from close")

    #         col11, col13 = st.beta_columns([4,3])
    #         with col11:
    #             st.write(filter_stock.upper())
    #             stock_fig = mpl.plot(data=chart_data[filter_stock.upper()], type=chart_type.lower(), style='yahoo', mav=(5,10,25), volume=True)
    #             st.pyplot(stock_fig)
    #             # fig = go.Figure(data=go.Candlestick(
    #             #     x=chart_data.index,
    #             #     open=chart_data[filter_stock.upper()]['Open'],
    #             #     high=chart_data[filter_stock.upper()]['High'],
    #             #     low=chart_data[filter_stock.upper()]['Low'],
    #             #     close=chart_data[filter_stock.upper()]['Close']))
    #             # fig.update_layout(
    #             #     autosize=False,
    #             #     width=900,
    #             #     height=800
    #             # )
    #             # st.plotly_chart(fig)
    #         with col13:
    #             st.write('Chart Data:')
    #             st.dataframe(chart_data[filter_stock.upper()], height=600)
    #             # st.write(chart_data[filter_stock.upper()])
    #         # with col10, col12, col14:
    #         #     st.write("")

    #         st.markdown("##")
    #         st.markdown("___")
           
    #         st.text_area(label=f"About {stock_data.info['shortName']}", value=stock_data.info['longBusinessSummary'], height=200)


    #         with st.beta_expander(label='Expand for Insider Trading (SEC Form 4):'):
    #             url = (f'http://openinsider.com/screener?s={filter_stock}&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1')
    #             read_insider = pd.read_html(url)
    #             insider = read_insider[-3].iloc[:,1:11]
    #             st.write(insider)



if __name__=='__main__':
    main()

