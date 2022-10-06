# Imports
import config
import supresistlines as supres
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
# import talib

today = pd.to_datetime(datetime.now(),utc=True).astimezone('Europe/London')
from_date = (today - relativedelta(weeks = 6)).astimezone('Europe/London')
gran = 'H4'
# print(today)
# print(from_date)

class PatternRecognition:
    def __init__(self,df,symbol, curr_date, start_date):
        self.df = df
        self.symbol = symbol
        self.curr_date = today
        self.start_date = from_date
        self.gran = gran
        self.df = supres.get_data(symbols=symbol, gran='H4', from_date=from_date)
        print(df)

    def hammer_scanner(self, buy, sell):
        for i in range(len(self)):
            
            # Hammer
            if self[i, 3] < self[i - 5, 3] and self[i, 3] > self[i, 0] \
                and self[i, 1] == self[i, 3]:
                self[i, buy] = 1
                
            # Inverted Hammer
            if self[i, 3] < self[i - 5, 3] and self[i, 3] > self[i, 0] \
                and self[i, 2] == self[i, 0]:
                self[i, buy] = 1
            
            # Hanging Man
            if self[i, 3] > self[i - 5, 3] and self[i, 3] < self[i, 0] \
                and self[i, 1] == self[i, 0]:
                self[i, sell] = -1
                
            # Shooting Star
            if Data[i, 3] < Data[i - 5, 3] and Data[i, 3] < Data[i, 0] \
                and Data[i, 2] == Data[i, 0]:
                Data[i, sell] = -1

    def three_candles__scanner(Data, buy, sell):
        for i in range(len(Data)):

            # Three White Soldiers
            if Data[i, 3] > Data[i - 1, 3] and Data[i - 1, 3] > Data[i - 2, 3] \
                and Data[i - 2, 3] > Data[i - 3, 3]:
                Data[i, buy] = 1
        
            # Three Black Crows
            if Data[i, 3] < Data[i - 1, 3] and Data[i - 1, 3] < Data[i - 2, 3] \
                and Data[i - 2, 3] < Data[i - 3, 3]:
                Data[i, sell] = -1

    def star_scanner(Data, buy, sell):
        
        for i in range(len(Data)):
            
            # Morning Star
            if Data[i, 3] > Data[i, 0] and Data[i, 0] > Data[i - 1, 3] \
                and Data[i - 1, 3] > Data[i - 1, 0] and Data[i - 1, 3] < Data[i - 2, 3]:
                Data[i, buy] = 1
            
            # Evening Star
            if Data[i, 3] < Data[i, 0] and Data[i, 0] < Data[i - 1, 3] \
                and Data[i - 1, 3] < Data[i - 1, 0] and Data[i - 1, 3] > Data[i - 2, 3]:
                Data[i, sell] = -1

    def piercing_cloud_scanner(Data, buy, sell):
        for i in range(len(Data)):
        
            # Piercing Pattern   
            if Data[i, 3] > Data[i, 0] and Data[i - 1, 3] < Data[i - 1, 0] \
                and Data[i, 3] < Data[i - 1, 0] and Data[i, 3] > Data[i - 1, 3] \
                    and  Data[i, 0] < Data[i - 1, 3]:
                Data[i, buy] = 1
            
            # Dark Cloud Pattern    
            if Data[i, 3] < Data[i, 0] and Data[i - 1, 3] > Data[i - 1, 0] \
                and Data[i, 3] > Data[i - 1, 0] and Data[i, 3] < Data[i - 1, 3] \
                    and Data[i, 0] > Data[i - 1, 3]:
                Data[i, sell] = -1

    def doji_scanner(Data, buy, sell):
        for i in range(len(Data)):
            
            # Bullish Doji    
            if Data[i - 1, 3] < Data[i - 1, 0 ] and Data[i, 3] == Data[i, 0]:
                Data[i, buy] = 1
            
            # Bearish Doji     
            if Data[i - 1, 3] > Data[i - 1, 0 ] and Data[i, 3] == Data[i, 0]:
                Data[i, sell] = -1

    def marubozu_scanner(Data, buy, sell):
        for i in range(len(Data)):
            
            # Bullish Marubozu      
            if Data[i, 3] > Data[i, 0] and Data[i, 3] == Data[i, 1] \
                and Data[i, 0] == Data[i, 2]:
                Data[i, buy] = 1
            
            # Bearish Marubozu      
            if Data[i, 3] < Data[i, 0] and Data[i, 3] == Data[i, 1] \
                and Data[i, 0] == Data[i, 2]:
                Data[i, sell] = -1

    def harami_scanner(Data, buy, sell):
        for i in range(len(Data)):
            
            if Data[i - 1, 3] < Data[i - 1, 0] and Data[i, 3] > Data[i, 0] \
                and Data[i - 1, 3] < Data[i, 2] and Data[i - 1, 0] > Data[i, 1]:
                Data[i, buy] = 1
                    
            if Data[i - 1, 3] > Data[i - 1, 0] and Data[i, 3] < Data[i, 0] \
                and Data[i - 1, 3] > Data[i, 1] and Data[i - 1, 0] < Data[i, 2]:
                Data[i, sell] = -1

    def three_methods_scanner(Data, buy, sell):
        for i in range(len(Data)):
            
            # Bullish Strike Method
            if Data[i, 3] > Data[i, 0] and Data[i - 1, 3] < Data[i - 1, 0] and Data[i - 2, 3] < Data[i - 2, 0] and \
                Data[i - 3, 3] < Data[i - 3, 0] and Data[i - 4, 3] > Data[i - 4, 0] and Data[i, 3] > Data[i - 3, 0] and \
                Data[i - 4, 0] < Data[i - 1, 3] and Data[i - 1, 3] < Data[i - 2, 3] and Data[i - 2, 3] < Data[i - 3, 3]:
                Data[i, buy] = 1
        
            # Bearish Strike Method
            if Data[i, 3] < Data[i, 0] and Data[i - 1, 3] > Data[i - 1, 0] and Data[i - 2, 3] > Data[i - 2, 0] and \
                Data[i - 3, 3] > Data[i - 3, 0] and Data[i - 4, 3] < Data[i - 4, 0] and Data[i, 3] < Data[i - 3, 0] and \
                Data[i - 4, 0] > Data[i - 1, 3] and Data[i - 1, 3] > Data[i - 2, 3] and Data[i - 2, 3] > Data[i - 3, 3]:
                Data[i, sell] = -1

    def strike_scanner(Data, buy, sell):
        for i in range(len(Data)):
                
                # Bullish Strike
                if Data[i, 3] > Data[i, 0] and Data[i - 1, 3] < Data[i - 1, 0] and Data[i - 2, 3] < Data[i - 2, 0] and \
                    Data[i - 3, 3] < Data[i - 3, 0] and Data[i - 1, 3] <    Data[i - 2, 3] and Data[i - 2, 3] < Data[i - 3, 3] and \
                    Data[i, 3] > Data[i - 3, 0]:
                    Data[i, buy] = 1
                
                # Bearish Strike
                if Data[i, 3] < Data[i, 0] and Data[i - 1, 3] > Data[i - 1,  0] and Data[i - 2, 3] > Data[i - 2, 0] and \
                    Data[i - 3, 3] > Data[i - 3, 0] and Data[i - 1, 3] > Data[i - 2, 3] and Data[i - 2, 3] > Data[i - 3, 3] and \
                    Data[i, 3] < Data[i - 3, 0]:
                    Data[i, sell] = -1

    def fibonacci_timing_pattern(Data, count, step, step_two, step_three, close, buy, sell):
    
        # Bullish Fibonacci Timing Pattern
        counter = -1
        for i in range(len(Data)):    
            if Data[i, close] < Data[i - step, close] and Data[i, close] < Data[i - step_two, close] \
                and Data[i, close] < Data[i - step_three, close]:
                Data[i, buy] = counter
                counter += -1 
                
                if counter == -count - 1:
                    counter = 0
                else:
                    continue   
                
            elif Data[i, close] >= Data[i - step, close]:
                counter = -1 
                Data[i, buy] = 0 
            
        # Bearish Fibonacci Timing Pattern
        counter = 1 
        
        for i in range(len(Data)):
            if Data[i, close] > Data[i - step, close] and Data[i, close] > Data[i - step_two, close] \
                and Data[i, close] > Data[i - step_three, close]: 
                print('we are here')
                Data[i, sell] = counter 
                counter += 1        
                
                if counter == count + 1: 
                    counter = 0            
                else:
                    continue   
                
            elif Data[i, date] <= Data[i - step, close]: 
                counter = 1 
                Data[i, sell] = 0 
        
        return Data

df = {}

symbols = supres.symbol('all')
for symbol in symbols:
    patrec = PatternRecognition(df, symbol, today, from_date)
    df= supres.get_data(symbols=symbol, gran='H4', from_date=from_date)
    df[symbol] = pd.DataFrame(df[symbol], index = df[symbol].index)
    hammer = patrec.hammer_scanner(df[symbol],buy= df, sell=df)
    # Using the function
    count = 8
    step = 5
    step_two = 3
    step_three = 2
    close = df[symbol]['Close']
    date = df[symbol].index
    df[symbol]['Buy'] = " "
    df[symbol]['Sell'] = " "
    print(df)
    # my_data = fibonacci_timing_pattern(df[symbol], count, step, step_two, step_three, close, df[symbol]['Buy'],df[symbol]['Sell'])
    patrec.hammer_scanner(df,symbol,df.Buy,df.Sell)