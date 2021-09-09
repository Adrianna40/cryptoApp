import get_data as gd
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# gd.request()
df = gd.create_df()
st.title('Crypto Price App')
st.markdown("""
This app retrieves cryptocurrency prices for the top cryptocurrency from the **nomics.com**!
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Data source:** [Nomics](https://nomics.com).
* **Credit:** Tutorial made with https://www.youtube.com/watch?v=JwSS70SZdyM
""")

col1 = st.sidebar
col2, col3 = st.columns((2, 1))

# Sidebar - Cryptocurrency selections
sorted_coin = sorted(df['id'])
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[(df['id'].isin(selected_coin))]  # Filtering data

# Sidebar - Number of coins to display
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

# 1d,7d,30d,365d,ytd
# Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                   ['1d', '7d', '30d', '365d', 'ytd'])
percent_dict = {"1d": '1d.price_change_pct',
                "7d": '7d.price_change_pct',
                "30d": '30d.price_change_pct',
                "365d": '365d.price_change_pct',
                "ytd": 'ytd.price_change_pct'}
selected_percent_timeframe = percent_dict[percent_timeframe]

# Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
df_show = pd.concat([df_coins['name'], df_coins['price'], df_coins['status']], axis=1)
col2.dataframe(df_show)

# Preparing data for Bar plot of % Price change
price_change_columns = ['1d.price_change_pct',
                        '7d.price_change_pct',
                        '30d.price_change_pct',
                        '365d.price_change_pct',
                        'ytd.price_change_pct']


percent_change_column = str(percent_timeframe) + '.price_change_pct'
df_coins[percent_change_column] = [float(x) for x in list(df_coins[percent_change_column])]

col2.subheader('Table of % Price Change')
df_change = pd.concat([df_coins['id'], df_coins[percent_change_column]], axis=1)
df_change = df_change.set_index('id')


positive_column = 'positive_percent_change_' + str(percent_timeframe)

df_change[positive_column] = [x > 0 for x in df_coins[percent_change_column]]
if sort_values == 'Yes':
    df_change = df_change.sort_values(by=[percent_change_column])
col2.dataframe(df_change)

# Conditional creation of Bar plot (time frame)
col3.subheader('Bar plot of % Price Change')

col3.write('*this is {} period*'.format(percent_timeframe))

plt.figure(figsize=(5, 25))
plt.subplots_adjust(top=1, bottom=0)
df_change[percent_change_column].plot(kind='barh', color=df_change[positive_column].map({True: 'g', False: 'r'}))
col3.pyplot(plt)
