'''
This class attempts to define all the listed pattern groups and group them with either a 
(1) for buy or (-1) indicating its a sell

The patterns act as confluence when used in conjunction with support or resistance lines and help
provide the user with a direction with which to place trade.
'''
from math import isclose

class CandlePatternRecognition:
    def __init__(self,df,symbol, curr_date, start_date, pips):
        self.df = df
        self.symbols = symbol
        self.curr_date = curr_date
        self.start_date = start_date
        self.df['Buy'] = " "
        self.df['Sell'] = " "
        self.pip_size = pips
        
    def doji(self):
        open = self.df['Open']
        close = self.df['Close']
        date = self.df.index

        for i in range(len(self.df)-1):
            if (float(open[i]) == float(close[i]) and \
                float(open[i - 1]) > float(close[i - 1]) and \
                    float(open[i - 2]) > float(close[i - 2])):
                # self.df['Buy'][i] = 1
                print(f'bull doji spotted at {self.symbols} on {date[i]} ')

            if (float(open[i]) == float(close[i]) and \
                float(close[i - 1]) > float(open[i - 1]) and \
                    float(open[i - 2]) > float(close[i - 2])):
                # self.df['Sell'][i] = -1
                print(f'bear doji found at {self.symbols} on {date[i]}')
            
        return self.symbols, date[i]

    def engulf(self):
        open = self.df['Open']
        close = self.df['Close']
        high = self.df['High']
        low = self.df['Low']
        date = self.df.index

        for i in range(len(self.df)-1): 
            max_bar = max(float(open[i]), float(close[i])) 
            max_bar_prev = max(float(open[i - 1]), float(close[i - 1]))
            max_bar_two = max(float(open[i - 2]), float(close[i - 2]))  
            low_bar = min(float(open[i]), float(close[i]))
            low_bar_prev = min(float(open[i - 1]), float(close[i - 1]))
            low_bar_two = min(float(open[i - 2]), float(close[i - 2]))
            body = max_bar - low_bar
            body_prev = max_bar_prev - low_bar_prev
            # body_two = max_bar_two - low_bar_two

           
            if (float(close[i]) > float(open[i]) and float(open[i - 1]) > float(close[i - 1]) and \
                float(open[i - 2]) > float(close[i - 2]) and float(close[i - 1]) < float(low[i - 2]) and \
                    float(body) > (200 * self.pip_size) and float(body) > (2 * float(body_prev))):
                # self.df['Buy'][i] = 1
                print(f'bullengulf found at {self.symbols} on {date[i]}')
            
            if(float(open[i]) > float(close[i]) and float(close[i - 1]) > float(open[i - 1]) and \
                float(close[i - 2]) > float(open[i - 2]) and float(close[i - 1]) > float(high[i - 2]) and \
                    float(body) > (200 * self.pip_size) and float(body) > (2 * float(body_prev))):
                # self.df['Sell'][i] = -1
                print(f'bearengulf found at {self.symbols} on {date[i]}')
                
        return self.symbols, date[i]

    def hammer(self):
        open = self.df['Open']
        close = self.df['Close']
        high = self.df['High']
        low = self.df['Low']
        date = self.df.index

        for i in range(len(self.df)-1):
            max_bar = max(float(open[i]), float(close[i])) 
            low_bar = min(float(open[i]), float(close[i]))
            upper_shadow = float(high[i]) - max_bar
            bottom_shadow = low_bar - float(low[i])

            if(float(high[i]) == float(close[i]) and \
                float(close[i - 1]) > float(open[i - 1]) and \
                    bottom_shadow > (200 * self.pip_size)):
                # self.df['Buy'][i] = 1
                print(f'hammer found  at {self.symbols} on {date[i]}')

            if(float(open[i]) == float(low[i]) and \
                float(close[i - 1]) > float(open[i - 1]) and \
                    upper_shadow > (200 * self.pip_size)):
                # self.df['Buy'][i] = 1
                print(f'inv hammer found at {self.symbols} on {date[i]}')
            
            if(float(close[i]) == float(low[i]) and \
                float(close[i - 1]) > float(open[i - 1]) and \
                    upper_shadow > (200 * self.pip_size)):
                # self.df['Sell'][i] = -1
                print(f'shooting star found at {self.symbols} on {date[i]}')

            if(float(open[i]) == float(high[i]) and \
                float(close[i - 1]) > float(open[i - 1]) and \
                    bottom_shadow > (200 * self.pip_size)):
                # self.df['Sell'][i] = -1
                print(f'hanging man found at {self.symbols} on {date[i]}')
                
        return self.symbols , date[i]

    def three_soldiers(self):
        open = self.df['Open']
        close = self.df['Close']
        high = self.df['High']
        low = self.df['Low']
        date = self.df.index

        for i in range(len(self.df)-1):
            max_bar = max(float(open[i]), float(close[i])) 
            max_bar_prev = max(float(open[i - 1]), float(close[i - 1]))
            max_bar_two = max(float(open[i - 2]), float(close[i - 2]))  
            low_bar = min(float(open[i]), float(close[i]))
            low_bar_prev = min(float(open[i - 1]), float(close[i - 1]))
            low_bar_two = min(float(open[i - 2]), float(close[i - 2]))
            body = max_bar - low_bar
            body_prev = max_bar_prev - low_bar_prev
            body_two = max_bar_two - low_bar_two
            # upper_shadow = float(high[i]) - max_bar
            upper_shadow_prev = float(high[i-1]) - max_bar_prev
            upper_shadow_two = float(high[i-2]) - max_bar_two
            # bottom_shadow = low_bar - float(low[i])
            bottom_shadow_prev = low_bar_prev - float(low[i-1])
            bottom_shadow_two = low_bar_two - float(low[i-2])
            half_body_candle = (body / 2) + low_bar 
            half_body_candle_prev = (body_prev /2) + low_bar_prev
            half_body_candle_two = (body_two /2) + low_bar_two

            if (float(open[i]) > float(open[i - 1]) and \
                float(open[i - 1]) > float(open[i - 2]) and \
                    float(close[i - 2]) >= half_body_candle_prev and \
                float(open[i]) >= half_body_candle_prev) and \
                    upper_shadow_prev < (50 * self.pip_size) and \
                        upper_shadow_two < (50 * self.pip_size):
                # self.df['Sell'][i] = -1
                print(f'three white soldiers found at {self.symbols} on {date[i]}')
            
            if(float(close[i]) < float(close[i - 1]) and \
                float(close[i - 1]) < float(close[i - 2]) and \
                    float(open[i - 1]) <= half_body_candle_two and\
                float(close[i - 1]) <= half_body_candle and \
                    bottom_shadow_prev < (50 * self.pip_size) and \
                        bottom_shadow_two < (50 * self.pip_size) ):
                # self.df['Buy'][i] = 1
                print(f'three black crows found at {self.symbols} on {date[i]}')
                
        return self.symbols, date[i] 

    def tweezers(self):
        open = self.df['Open']
        close = self.df['Close']
        high = self.df['High']
        low = self.df['Low']
        date = self.df.index

        for i in range(len(self.df)-1):
            
            if (float(close[i-1]) == float(open[i]) and float(high[i-1]) == float(open[i-1])  and\
                float(close[i]) == float(high[i]) and float(close[i]) > float(open[i]) and\
                float(open[i-1]) > float(close[i-1]) and float(open[i-2]) > float(close[i-2]) and\
                float(open[i-3]) > float(close[i-3])):
                # self.df['Buy'][i] = 1
                print(f'tweezer bottoms found at {self.symbols} on {date[i]}')

            if (float(open[i-1]) == float(close[i]) and float(low[i-1]) == float(open[i-1])  and\
                float(close[i]) == float(low[i]) and float(open[i]) > float(close[i]) and \
                float(close[i-1]) > float(open[i-1]) and float(close[i-2]) > float(open[i-2]) and\
                float(close[i-3]) > float(open[i-3])):
                # self.df['Sell'][i] = -1
                print(f'tweezer tops found at {self.symbols} on {date[i]}')

        return self.symbols, date[i]
        