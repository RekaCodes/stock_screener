import streamlit as st
st.set_page_config(layout='centered')
import pandas as pd
import matplotlib.pyplot as plt
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

    filter_period = '6mo'
    filter_interval = '1d'
    chart_type = 'candle'

    col1, col2 = st.beta_columns([1,3])
    with col1:
        filter_stock = st.text_input(label="", value='AAPL')
    with col2:
        st.write("")
    if st.button('Get stock data'):
        chart_data=yf.download([filter_stock.upper(), 'SPY'], period=filter_period, interval=filter_interval, group_by='ticker', auto_adjust=True)
        stock_data = yf.Ticker(filter_stock.upper())

        st.header(stock_data.info['shortName'])

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
            # st.write(stats_data.iloc[1,[filter_stock.upper()]['Close']])
            # st.write('Change from Close ')
        # st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
            st.header(f"{chg_frm_close} {pct_chg_frm_close}")
            st.write("Change from close")
            # st.header('{:.1%}'.format(chg_frm_close))


        stock_fig = mpl.plot(data=chart_data[filter_stock.upper()], type=chart_type.lower(), style='yahoo', mav=(5,10,25), volume=True, title=filter_stock.upper())
        st.pyplot(stock_fig)

        st.write(stock_data.info)

        with st.beta_expander(label='Click for data'):
            st.write(chart_data[filter_stock.upper()])


if __name__=='__main__':
    main()

