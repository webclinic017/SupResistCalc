# Imports
from datetime import datetime
from xmlrpc.client import DateTime
import  requests, config
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pytz

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
    df = {}
    tz = pytz.timezone('Europe/London')
    df[symbols] = pd.DataFrame(
        pd.json_normalize(requests.get(f'{config.oanda_candles}/{symbols}/candles?count={count}&from={from_date}&granularity={gran}',
    headers =config.oanda_headers).json(),max_level=1, 
    record_path = ['candles'], errors='ignore'))
    # print(df.items())
    # tz.localize(df[symbols]['time'])
    df[symbols] = df[symbols].loc[:,['time','mid.o','mid.h','mid.l','mid.c','volume']]
    df[symbols].rename(columns={'time':'Date', 'mid.o':'Open','mid.h':'High','mid.l':'Low','mid.c':'Close','volume':'Volume'},inplace=True)
    df[symbols]['Date'] = pd.to_datetime(df[symbols]['Date'])
    df[symbols] = df[symbols].set_index(['Date'])
    return df

# Plots candlestick charts and adds Support Resistence lines
def plot_charts(symbols, df, gran,levels):
    fig = go.Figure(data= go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        increasing_line_color="green",
        decreasing_line_color="red",
        name='Price',

        ))
                                
    n = 0
    support_resistance_prices =""
    for level in levels:
        c0 = df.index[level[0]-1]
        t0 = level[1]
        c1 = df.index[len(df)-1]
        t1 = level[1]
    
        fig.add_traces(go.Scatter(
            x=[c0,c1],
            y =[t0,t1],
            line= dict(dash='dash', width=3),
            name=f'Sup + Resist Lines {n}'
            ))
        n+=1
         
        support_resistance_prices = "{:.5f}".format(float(level[1]))
        fig.add_annotation(
            text=support_resistance_prices,
            align='left',
            showarrow=False,
            x=c0,
            y= t1)

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
    )
    fig.show()
    # pprint(fig)

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
                   level in levels]) ==1

# Determines if a breakout has occured
def has_breakout(levels, previous, last):
    for _, level in levels:
        cond1 = (float(previous['Open']) < float(level)) # to make sure previous candle is below level
        cond2 = (float(last['Open']) > float(level)) and (float(last['Low']) > float(level))
    return cond1 and cond2

# Method 1: Using Fractal candlestick pattern
def detect_level_method_1(df):
    # df = pd.DataFrame(df,df.index)
    levels = []
    for i in range(2, df.shape[0] -2):
        if is_support(df, i):
            l = float(df['Low'][i])
            if is_far_from_level(l, levels, df):
                levels.append((i, l))
        elif is_resistance(df,i):
            l = float(df['High'][i])
            if is_far_from_level(l, levels, df):
                levels.append((i,l))
    return levels


# Method 2: Window shifting method
def detect_level_method_2(df):
    max_list = []
    min_list = []
    levels = []
    # df = pd.DataFrame(df,df.index)
    for i in range(5, df.shape[0] -5):
        high_range = df['High'][i-5:i+4].astype(float)
        current_max = high_range.max()
        
        if current_max not in max_list:
            max_list = []
        max_list.append(current_max)

        if len(max_list) == 5 & is_far_from_level(current_max,levels, df):
            levels.append((i, current_max))

        low_range = df['Low'][i-5:i+5].astype(float)
        current_min = low_range.min()

        if current_min not in min_list:
            min_list = []
        min_list.append(current_min)

        if len(min_list) == 5 & is_far_from_level(current_min,levels, df):
            levels.append((i, current_min))
    return levels

