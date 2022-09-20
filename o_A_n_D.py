# Imports
from __future__ import annotations
from itertools import count
from xmlrpc.client import DateTime
import oandapyV20
import oandapyV20.endpoints.forexlabs as labs
import oandapyV20.endpoints.instruments as instruments
import  requests, config
import pandas as pd
from typing import  OrderedDict
import numpy as np
import plotly.graph_objects as go

# Function to define the symbols or pairs used
def symbol(sym):
    if sym == 'all':
        symbol = pd.json_normalize(requests.get(f"{config.oanda_url}/instruments/",
        headers=config.oanda_headers).json(),max_level=2,
        record_path = ['instruments'])
        symbols = symbol.name
    
    else:
        symbols = [sym]

    return symbols

# Takes Symbols and passes it through Oanda API to get predetermined history
# Cleans dataframe into usable format
def get_data(symbols, gran, from_date):
    count = 1000
    dt_from = DateTime(from_date)
    df = OrderedDict()
    df[symbols] = pd.DataFrame(
        pd.json_normalize(requests.get(f'{config.oanda_candles}/{symbols}/candles?count={count}&from={dt_from}&granularity={gran}',
    headers =config.oanda_headers).json(),max_level=1, 
    record_path = ['candles'], errors='ignore')
    )
    df[symbols] = df[symbols].loc[:,['time','mid.o','mid.h','mid.l','mid.c','volume']]
    df[symbols].rename(columns={'time':'Date', 'mid.o':'Open','mid.h':'High','mid.l':'Low','mid.c':'Close','volume':'Volume'},inplace=True)
    df[symbols]['Open'].astype(float)
    df[symbols]['High'].astype(float)
    df[symbols]['Low'].astype(float)
    df[symbols]['Close'].astype(float)
    df[symbols]['Volume'].astype(float)
    df[symbols] = df[symbols].set_index(['Date'])
    # df[symbols].index = pd.DatetimeIndex(df[symbols].index).strftime('%d-%m-%Y %H:%M:%S')
    return df

# Plots candlestick charts and adds Support Resistence lines
def plot_charts(symbols, df, gran,levels):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,
                                open=df['Open'],
                                close=df['Close'],
                                low=df['Low'],
                                high=df['High'],
                                increasing_line_color="green",
                                decreasing_line_color="red",name='Price'))

    i = 0 
    support_resistance_prices = ""
    for level in levels:
        x0 = df.index[level[0]-1]
        y0 = level[1]
        x1 = df.index[len(df)-2]
        y1 = level[1]

        fig.add_trace(go.Scatter(
            name=f'Support and Resistance {i}',
            mode='lines',
            y=[ y0, y1] , x = [x0 , x1] 
            ))
        i+=1
            
        support_resistance_prices = "{:.2f}".format(level[0])
        fig.add_annotation(text=support_resistance_prices,
                       align='center',
                       showarrow=True,
                       xref='paper',
                       yref='paper',
                       x=0.1,
                       y=0.9+i,
                       bordercolor='pink',
                       borderwidth=3)

    fig.update_layout(
        title = f'{symbols} "{gran}" Charts',
        yaxis_title = f'{symbols} Price',
        xaxis_title = 'Date',
        paper_bgcolor= 'black',
        plot_bgcolor= 'black',
        font_color= 'darkgray',
        font_family= 'tahoma',
        font_size = 14,
        xaxis=dict(showgrid = False,showticklabels=True),
        yaxis=dict(showgrid=False,showticklabels=True),
        legend_title_font_color = 'lightgray',
        showlegend = True,
        legend= dict(
            title='Support & Resistance Lines',
            font = dict(
                size = 12,
                color = 'lightgray',
                family = 'tahoma', 
        )),
        # shapes= [dict(
        #     type='line',
        #     x0 = df.index[len(df)-1], x1 = df.index[level[0]-1],
        #     y0 = level[1], y1= level[1], xref='x', yref='y',
        #     line_width = 3)],
            
        # annotations = [dict(
        #     text = f'{level[1]}'
        # )]
    )

    fig.show()

# Determines if there is Support
def is_support(df, i):
    cond1 = df['Low'][i] < df['Low'][i-1]
    cond2 = df['Low'][i] < df['Low'][i+1]
    cond3 = df['Low'][i] < df['Low'][i+2]
    cond4 = df['Low'][i] < df['Low'][i-2]
    return cond1 and cond2 and cond3 and cond4

# Determines if there is Resistance
def is_resistance(df,i):
    cond1 = df['High'][i] > df['High'][i-1]
    cond2 = df['High'][i] > df['High'][i+1]
    cond3 = df['High'][i] > df['High'][i+2]
    cond4 = df['High'][i] > df['High'][i-2]
    return cond1 and cond2 and cond3 and cond4 

# Creates a distance between levels to quieten the noise
def is_far_from_level(value,levels,df):
    ave = np.mean(df['High'].astype(float) - df['Low'].astype(float))
    return np.sum([abs(float(value) - float(level)) < ave for _, 
                   level in levels]) ==0

# Looks for price range within a level to initiate trade logic
def is_within_level(value,levels,df):
    ave = np.mean(df['High'].astype(float) - df['Low'].astype(float))
    return np.sum([abs(float(value) - float(level)) > ave for _, 
                   level in levels]) ==0

# Determines if a breakout has occured
def has_breakout(levels, previous, last):
    for _, level in levels:
        cond1 = (float(previous['Open']) < float(level)) # to make sure previous candle is below level
        cond2 = (float(last['Open']) > float(level)) and (float(last['Low']) > float(level))
    return cond1 and cond2

# Method 1: Using Fractal candlestick pattern
def detect_level_method_1(df):
    levels = []
    for i in range(2, len(df) -2):
        if is_support(df, i):
            l = df['Low'][i]
            if is_far_from_level(l, levels, df):
                levels.append((i, l))
        elif is_resistance(df,i):
            l = df['High'][i]
            if is_far_from_level(l, levels, df):
                levels.append((i,l))
    return levels

# Method 2: Window shifting method
def detect_level_method_2(df):
    levels = []
    max_list = []
    min_list = []
    df[sym] = pd.DataFrame(df[sym],df[sym].index)
    for i in range(5, df[sym].shape[0] -5):
        high_range = df[sym]['High'][i-5:i+4].astype(float)
        current_max = high_range.max()
        
        if current_max not in max_list:
            max_list = []
        max_list.append(current_max)

        if len(max_list) == 5 & is_far_from_level(current_max,levels, df[sym]):
            levels.append((high_range.idxmax(), current_max))

        low_range = df[sym]['Low'][i-5:i+5].astype(float)
        current_min = low_range.min()

        if current_min not in min_list:
            min_list = []
        min_list.append(current_min)
        # print(f' min_list = {min_list} for symbol {sym}')

        if len(min_list) == 5 & is_far_from_level(current_min,levels, df[sym]):
            levels.append((low_range.idxmin(), current_min))
    return levels

# lists to store the screened results
screened_list_1 = [] 
screened_list_2 = []


# # Drawing support and resistance lines on all the charts
# symbols = symbol('GBP_USD')
# gran = 'H4'
# from_date = '2022-03-01'

# for sym in symbols:
#     try:
#         data = get_data(sym, gran=gran,from_date=from_date)
#         levels = [] 
#         for i in range(2, len(data[sym]) - 2):
#             if is_support(data[sym],i):
#                 l = data[sym]['Low'][i]
#                 if is_far_from_level(l, levels, data[sym]):
#                     levels.append((i,l))
#             elif is_resistance(data[sym],i):
#                 l = data[sym]['High'][i]
#                 if is_far_from_level(l, levels, data[sym]):
#                     levels.append((i, l))
#         plot_charts(sym, data[sym], gran,levels=levels)
#     except Exception as e:
#         print(e)

# Initiating the code
symbols = symbol('all')
gran = 'D'
from_date = '2022-03-01'
for sym in symbols:
    try:
        df = get_data(symbols=sym,gran=gran,from_date= from_date)
        # df[sym] = pd.DataFrame(df[sym], index = df[sym].index)

        levels_1 = detect_level_method_1(df[sym])
        if (has_breakout(levels_1[-5:],df[sym].iloc[-2], df[sym].iloc[-1])):
            screened_list_1.append(sym)

        df[sym] = pd.DataFrame(df[sym], index = df[sym].index)
        levels_2 = detect_level_method_2(df)
        if (has_breakout(levels_2[-5:],df[sym].iloc[-2], df[sym].iloc[-1])):
            screened_list_2.append(sym)
        
    except Exception as e:
        print(f'error - {e}')

print(f'screened 1 = {screened_list_1}')
print(f'screened 2 = {screened_list_2}')

# Method 1: Using Fractal candlestick pattern (After the screener has run)
for stock_code in screened_list_1:
    df = get_data(stock_code, gran=gran,from_date= from_date)
    levels = []
    for i in range(2, len(df[stock_code]) - 2):
        if is_support(df[stock_code],i):
            l = df[stock_code]['Low'][i]
            if is_far_from_level(l, levels, df[stock_code]):
                levels.append((i,l))
        elif is_resistance(df[stock_code], i):
            l = df[stock_code]['High'][i]
            if is_far_from_level(l, levels, df[stock_code]):
                levels.append((i, l))

    plot_charts(symbols=stock_code, df=df[stock_code], gran=gran,levels=levels)

# Method 2: Window shifting method (After the screener has run)
for symbols in screened_list_2:
    df = get_data(symbols, gran=gran, from_date=from_date)
    pivots = []
    max_list = []
    min_list = []
    for i in range(5, len(df[symbols])-5):
        high_range = df[symbols]['High'][i-5:i+4].astype(float)
        current_max = high_range.max()

        if current_max not in max_list:
            max_list = []
        max_list.append(current_max)

        if len(max_list) == 5 and is_far_from_level(current_max,pivots, df[symbols]):
            pivots.append((i, current_max))

        low_range = df[symbols]['Low'][i-5:i+4].astype(float)
        current_min = low_range.min()
        if current_min not in min_list:
            min_list = []
        min_list.append(current_min)

        if len(min_list) == 5 and is_far_from_level(current_min, pivots,df[symbols]):
            pivots.append((i, current_min))

    plot_charts(symbols=symbols, df=df[symbols],gran=gran,levels=pivots)
