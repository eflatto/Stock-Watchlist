import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

from streamlit_option_menu import option_menu



import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

 
st.set_page_config(
    page_title = "Finance",
    page_icon ="💵",
    initial_sidebar_state="expanded",
    menu_items = {
        'Get Help': 'https://docs.streamlit.io/',
        'Report a Bug': 'https://www.edwinflatto.com',
        'About': 'Developed by Edwin Flatto'
    }
)

selected = option_menu(
    menu_title=None,
    options=["Log In", "Crypto", "Stocks", "Sign Up", "Support"],
    icons=["house", "currency-bitcoin", "activity", "person-lines-fill", "chat-square-dots"],
    default_index=0,
    orientation="horizontal",
)


#Home Page
if selected == "Log In":
    st.image("media/Home.png")

    form = st.form(key='my-form')
    log_in = form.subheader("Log In")
    username = form.text_input("*Username")
    password = form.text_input("*Password",type='password')
    submit = form.form_submit_button('Log In')
    create_usertable()
    hashed_pswd = make_hashes(password)
    result = login_user(username, password)

    if result:
        log_in = form.success("Welcome back, {}".format(username), icon="✅")

    else:
        error_msg = form.error("Incorrect Username/Password", icon="🚨")

    st.image("media/Phone.png")
    st.markdown('<div style="text-align: center;">The stock market is right at your fingertips.</div>', unsafe_allow_html=True)


#Crypto Page
if selected == "Crypto":
    st.image("media/Crypto.png")
    st.subheader("Learn More About Your Favorite Cryptocurrency and Compare it to Other Crypto Below.")

    tickers = ('BNB-USD', 'BTC-USD', 'DOGE-USD', 'ETH-USD', 'LINK-USD', 'LTC-USD', 'SOL-USD', 'XRP-USD')
    dropdown = st.multiselect("Pick your asset(s)", tickers)
    start = st.date_input('Start', value = pd.to_datetime('2022-01-01'))
    end = st.date_input('End', value = pd.to_datetime('today'))

    if len(dropdown) == 1:
        df = yf.download(dropdown, start, end)['Adj Close']
        area_df = yf.download(dropdown, start, end)['Volume']
        tableDf = yf.download(dropdown, start, end)
        st.dataframe(tableDf, width=1000, height=200)
        st.header("Prices of {}".format(dropdown))
        st.line_chart(df)
        st.header("Volume of {}".format(dropdown))
        st.area_chart(area_df)

    if len(dropdown) > 1:
        df = yf.download(dropdown, start, end)['Adj Close']
        area_df = yf.download(dropdown, start, end)['Volume']
        tableDf = yf.download(dropdown, start, end)
        st.dataframe(tableDf, width=1000, height=200)
        st.header("Compared Prices Between {}".format(dropdown))
        st.line_chart(df)
        st.header("Compared Volume Between {}".format(dropdown))
        st.area_chart(area_df)



#Stocks Page
if selected == "Stocks":
    st.image("media/Stocks.png")
    st.subheader("Learn More About Your Favorite Stock and Compare it to Other Stocks Below.")
    tickers = ('AAPL', 'AMZN', 'NIO', 'GOOGL', 'TSLA', 'NVDA', 'MSFT')
    dropdown = st.multiselect("Pick your asset(s)", tickers)
    start = st.date_input('Start', value=pd.to_datetime('2022-01-01'))
    end = st.date_input('End', value=pd.to_datetime('today'))


    if len(dropdown) == 1:
        df = yf.download(dropdown, start, end)['Adj Close']
        area_df = yf.download(dropdown, start, end)['Volume']
        tableDf = yf.download(dropdown, start, end)
        st.dataframe(tableDf, width=1000, height=200)
        st.header("Prices of {}".format(dropdown))
        st.line_chart(df)
        st.header("Volume of {}".format(dropdown))
        st.area_chart(area_df)

    if len(dropdown) > 1:
        df = yf.download(dropdown, start, end)['Adj Close']
        area_df = yf.download(dropdown, start, end)['Volume']
        tableDf = yf.download(dropdown, start, end)
        st.dataframe(tableDf, width=1000, height=200)
        st.header("Compared Prices Between {}".format(dropdown))
        st.line_chart(df)
        st.header("Compared Volume Between {}".format(dropdown))
        st.area_chart(area_df)

#Sign Up Page
if selected == "Sign Up":
    st.image("media/Sign Up.png")
    st.subheader("If you do not already have an account with us, please fill out the form below.")
    c1, c2 = st.columns(2)

    with c1:
        first_name = st.text_input("*First Name")
    with c2:
        last_name = st.text_input("*Last Name")

    address = st.text_input("*Full Address")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        apt_num = st.text_input("Apt. Number")
    with col2:
        state = st.text_input("*State")
    with col3:
        city = st.text_input("*City")
    with col4:
        zip_code = st.text_input("*Zip Code")
    email = st.text_input("*Email")
    new_user = st.text_input("*Username")
    new_password = st.text_input("*Password", type='password')
    newsletter = st.checkbox("Opt for newsletter")
    submit = st.button('Sign Up')

    if first_name and last_name and address and state and city and zip_code and new_user and email and new_password:
        create_usertable()
        add_userdata(new_user, new_password)
        sign_up = st.success("Thank you for creating an account with us, {}".format(new_user), icon="✅")
        success_sign = st.info("Go to Log In Page")
    elif submit:
        error_msg1 = st.error("Please input information into all the *mandatory text fields", icon="🚨")


#Support Page
if selected == "Support":
    st.image("media/Support.png")

    form = st.form(key='my-form')
    user_name = form.text_input("*Your Full Name")
    email_address = form.text_input("*Your Email Address")
    inquiry = form.text_area(label='*Input Request/ Inquiry')
    form.write("Please describe your request/ inquiry in detail")
    submit = form.form_submit_button('Submit')
    if user_name and email_address and inquiry:
        sign_up = form.success("The team will get back to you shortly", icon="✅")
    elif submit:
        empty_email = form.error("Please input information into all the *mandatory text fields", icon="🚨")

    st.image("media/Divider.png")
    st.subheader("Contact")
    st.write("Email: eflat003@fiu.edu")
    st.write("Headquarter Address: 11200 SW 8th St, Miami, FL 33199")
    map_data = pd.DataFrame(
        np.array([
            [25.756304, -80.375717]]),
        columns=['lat', 'lon'])
    st.map(map_data)
    st.radio("Would you recommend our website to others?",
             ["Yes", "No"])