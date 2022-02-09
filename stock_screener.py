from numpy.core.fromnumeric import size
import streamlit as st
st.set_page_config(layout='wide')
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
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
    chart_type = 'candle'
    filter_period = '6mo'
    filter_interval = '1d'

    
    col4, col5 = st.sidebar.columns(2)
    with col4:
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
        chart_type = st.radio('Chart Type:',['Candle', 'OHLC', 'Line', 'PNF'])
    with col5:
        st.write("")
        filter_time_frame = st.selectbox(
        "Time Frame",
        ['1D:5m', '5D:1h', '1Mo:1d', '3Mo:1d', '6Mo:1d', '1Y:1wk', '2Y:1wk'],
        index=4
        )
    st.markdown("##")

    filter_period = filter_time_frame.split(":")[0].lower()
    filter_interval = filter_time_frame.split(":")[1].lower()
    

    if st.sidebar.button('Lookup Stock'):
        if filter_stock=="":
            st.warning("Don't forget to enter a ticker symbol.")
        else:
            with st.spinner("Wait for it....!"):
                # if st.button('Get stock data'):
                    chart_data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)
                    stock_data = yf.Ticker(filter_stock.upper())
                    try:                    
                        st.header(f"{stock_data.info['shortName']}")
                    except HTTPError:
                        st.write('You forgot to enter a ticker!')


                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.title('${:0,.2f}'.format(stock_data.info['ask']))
                    
                    with col3:
                        st.write('52W High| ${:0,.2f}'.format(stock_data.info['fiftyTwoWeekHigh']))
                        st.write('52W Low| ${:0,.2f}'.format(stock_data.info['fiftyTwoWeekLow']))

                    with col2:
                        close_prior = stock_data.info['previousClose']
                        ask_current = stock_data.info['ask']
                        chg_frm_close = ask_current - close_prior
                        pct_chg_frm_close = chg_frm_close/close_prior
                        chg_frm_close = "${:0,.2f}".format(chg_frm_close).replace('$-','-$')
                        pct_chg_frm_close = "{:.1%}".format(pct_chg_frm_close).replace('$-','-$')

                        st.header(f"{chg_frm_close}  ({pct_chg_frm_close})")
                        st.write("Change from close")

                    
                    st.write("")

                    stock_fig = plt.figure(figsize=(16,7))
                    ax = stock_fig.add_subplot(111)
                    mpl.plot(data=chart_data[filter_stock.upper()], type=chart_type.lower(), style='yahoo', mav=(5,10,25), ax=ax)
                    
                    from matplotlib.offsetbox import AnchoredText
                    at = AnchoredText(
                        f"{filter_stock.upper()}",
                        loc='upper left',
                        frameon=False,
                        prop=dict(fontsize=42, fontweight='bold', alpha=0.15, color='slategrey'))
                    ax.add_artist(at)
                    st.pyplot(stock_fig)
                    
                    
                    st.markdown("___")

                    st.text_area(label=f"About {stock_data.info['shortName']}", value=stock_data.info['longBusinessSummary'], height=200)
                    # st.write(stock_data.info) << keep for future features


                    st.markdown("###")

                    with st.expander(label='Expand for Insider Trading (SEC Form 4):'):
                        url_insiders = (f'http://openinsider.com/screener?s={filter_stock}&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1')
                        read_insider = pd.read_html(url_insiders)
                        insider = read_insider[-3].iloc[:,1:12]
                        st.write(insider)


    st.sidebar.write("___")


    ## Screener ##

    slct_screener = st.sidebar.selectbox(
    label='Select a Screening Strategy',
    options=['New Highs', 'New Lows', 'High Dividend Yield', 'Most Active', 'Undervalued', 'Insider Trading'],
    index=0
    )

    if st.sidebar.button("Run Screening Strategy"):
    #     if slct_screener=='High Dividend Yield':
    #         read_highdiv = pd.read_html('https://finviz.com/screener.ashx?v=160&f=fa_div_high,idx_sp500&ft=4&o=-dividendyield')
    #         highdiv = read_highdiv[-1]
    #         st.write(highdiv)
        if slct_screener=='Insider Trading':
            st.header("Latest Insider Trading")
            read_ins_trading = pd.read_html('http://openinsider.com/latest-insider-trading')
            ins_trading = read_ins_trading[-3].iloc[:,1:13]
            st.dataframe(ins_trading, height=550)
        else:
        st.warning(f"You chose the {slct_screener} strategy, which hasn't been implemented yet. For now select Latest Insider Trading or type a stock symbol above.")

 

if __name__=='__main__':
    main()

