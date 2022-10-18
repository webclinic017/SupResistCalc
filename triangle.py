import numpy as np
import supresistlines as supres
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta,date
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt

today = (pd.to_datetime(datetime.today(),utc=True).astimezone('Europe/London'))
from_date = (today - relativedelta(months = 6)).astimezone('Europe/London')
symbols = supres.symbol('GBP_USD')
def triangle_patterns(df):
    prices_low,prices_high,prices_close=[],[],[]
    for i in range(200,1,-1):
        try:
            prices_high.append(float(df.High[i]))
            prices_low.append(float(df.Low[i]))
            prices_close.append(float(df.Close[i]))
        except:
            continue
    prices_low=np.array(prices_low)
    prices_high=np.array(prices_high)

    local_min_idx=argrelextrema(prices_low,np.less)[0]
    local_max_idx=argrelextrema(prices_high,np.greater)[0]
    local_min_idx=np.array(local_min_idx)
    local_max_idx=np.array(local_max_idx)

    local_min=[]
    local_max=[]
    for loc in local_min_idx:
        local_min.append(prices_low[loc])
    for loc in local_max_idx:
        local_max.append(prices_high[loc])
    local_min=np.array(local_min)
    local_max=np.array(local_max)
    for i in range(0,len(local_max)-3):
        (m,c),r,_,_,_= np.polyfit(local_max_idx[i:i+3],local_max[i:i+3],1,full=True)
        if(m<=3 and m>=-3 and (r[0]<20 and r[0]>-20)):
            start=local_max_idx[i+2]
            for k in range(start,start+7):
                if(k<len(prices_close) and prices_close[k]>(k*m+c)):
                    plt.figure(figsize=(10,5))
                    plt.plot(local_max_idx,m*local_max_idx+c,'m')
                    plt.plot(prices_close)
                    plt.plot(k,prices_close[k],'bo')
                    plt.title(symbol)
                    plt.show()
                    break
for symbol in symbols:
    df = supres.get_data(symbols=symbol,gran='D',from_date=from_date)
    triangle = triangle_patterns(df[symbol])
