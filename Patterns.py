'''
This class attempts to define all the listed pattern groups and group them with either a 
(1) for buy or (-1) indicating its a sell

The patterns act as confluence when used in conjunction with support or resistance lines and help
provide the user with a direction with which to place trade.
'''
class PatternRecognition:

    def __init__(self,df,symbol, curr_date, start_date, pips):
        self.df = df
        self.symbols = symbol
        self.curr_date = curr_date
        self.start_date = start_date
        self.df['Buy'] = " "
        self.df['Sell'] = " "
        self.pip_size = pips

    def doji(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            two_candles = i-2

            if (float(open[curr_candle]) == float(close[curr_candle]) and \
                float(open[previous_candle]) > float(close[previous_candle]) and \
                    float(open[two_candles]) > float(close[two_candles])):
                # self.df['Buy'][i] = 1
                print(f'bull doji spotted at {self.symbols} on {self.df.index[i]} ')
                # np.where(open[i] == close[i], print(f'doji found on {self.symbols} at {i}'),nan)
                # return self.symbols, self.df.index[i]

            if (float(open[curr_candle]) == float(close[curr_candle]) and \
                float(close[previous_candle]) > float(open[previous_candle]) and \
                    float(open[two_candles]) > float(close[two_candles])):
                # self.df['Sell'][i] = -1
                print(f'bear doji found at {self.symbols} on {self.df.index[i]}')
            
        return self.symbols, self.df.index[i]

    def engulf(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high= self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            two_candles = i-2
            max_bar_curr_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            max_bar_prev_bar = max(float(open[previous_candle]), float(close[previous_candle]))
            low_bar_curr_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            low_bar_prev_bar = min(float(open[previous_candle]), float(close[previous_candle]))
            body1 = max_bar_curr_bar - low_bar_curr_bar
            body2 = max_bar_prev_bar - low_bar_prev_bar
            
            if (close[curr_candle] > open[curr_candle] and open[previous_candle] > close[previous_candle] and \
                open[two_candles] > close[two_candles] and close[previous_candle] < low[two_candles] and \
                    body1 > (200 * self.pip_size) and body1 > (2 * body2)):
                # self.df['Buy'][i] = 1
               
                print(f'bullengulf found at {self.symbols} on {self.df.index[i]}')
                # return self.symbols, self.df.index[i]
            
            if(open[curr_candle] > close[curr_candle] and close[previous_candle] > open[previous_candle] and \
                close[two_candles] > open[two_candles] and close[previous_candle] > high[two_candles] and \
                    body1 > (200 * self.pip_size) and body1 > (2 * body2)):
                # self.df['Sell'][i] = -1
                
                print(f'bearengulf found at {self.symbols} on {self.df.index[i]}')
                
        return self.symbols, self.df.index[i]

    def hammer(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            # two_candles = i-2
            max_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            low_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            top_shadow = float(high[curr_candle]) - max_bar
            bottom_shadow = low_bar - float(low[curr_candle])
            body1 = ((max_bar - low_bar) * self.pip_size)

            if(float(high[curr_candle]) == float(close[curr_candle]) and \
                float(close[previous_candle]) > float(open[previous_candle]) and \
                    bottom_shadow > (200 * self.pip_size)):
                # self.df['Buy'][i] = 1
                print(f'hammer found  at {self.symbols} on {self.df.index[i]}')

            if(float(open[curr_candle]) == float(low[curr_candle]) and \
                float(close[previous_candle]) > float(open[previous_candle]) and \
                    top_shadow > (200 * self.pip_size)):
                # self.df['Buy'][i] = 1
                print(f'inv hammer found at {self.symbols} on {self.df.index[i]}')
            
            if(float(close[curr_candle]) == float(low[curr_candle]) and \
                float(close[previous_candle]) > float(open[previous_candle]) and \
                    top_shadow > (200 * self.pip_size)):
                # self.df['Sell'][i] = -1
                print(f'shooting star found at {self.symbols} on {self.df.index[i]}')

            if(float(open[curr_candle]) == float(high[curr_candle]) and \
                float(close[previous_candle]) > float(open[previous_candle]) and \
                    bottom_shadow > (200 * self.pip_size)):
                # self.df['Sell'][i] = -1
                print(f'hanging man found at {self.symbols} on {self.df.index[i]}')
                
        return self.symbols , self.df.index[i]

    def three_soldiers(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i -1
            two_candles = i -2
            max_bar_curr_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            max_bar_prev_bar = max(float(open[previous_candle]), float(close[previous_candle]))
            max_bar_two_bar = max(float(open[two_candles]), float(close[two_candles]))
            low_bar_curr_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            low_bar_prev_bar = min(float(open[previous_candle]), float(close[previous_candle]))
            low_bar_two_bar = min(float(open[two_candles]), float(close[two_candles]))
            half_body_candle_1 = ((max_bar_curr_bar - low_bar_curr_bar)/2) + low_bar_curr_bar
            half_body_candle_2 = ((max_bar_prev_bar - low_bar_prev_bar)/2) + low_bar_prev_bar
            half_body_candle_3 = ((max_bar_two_bar - low_bar_two_bar)/2) + low_bar_two_bar
            top_shadow_1 = float(high[curr_candle]) - max_bar_curr_bar
            top_shadow_2 = float(high[previous_candle]) - max_bar_prev_bar
            top_shadow_3 = float(high[two_candles]) - max_bar_two_bar
            bottom_shadow_1 = float(close[curr_candle]) - low_bar_curr_bar
            bottom_shadow_2 = float(close[previous_candle]) - low_bar_prev_bar
            bottom_shadow_3 = float(close[two_candles]) - low_bar_two_bar

            if (float(open[curr_candle]) > float(open[previous_candle]) and \
                float(open[previous_candle]) > float(open[two_candles]) and \
                    float(close[two_candles]) >= half_body_candle_2 and\
                float(open[curr_candle]) >= half_body_candle_2) and \
                    top_shadow_1 < (50 * self.pip_size) and top_shadow_2 < (50 * self.pip_size) and \
                        top_shadow_3 < (50 * self.pip_size):
                print(f'three white soldiers found at {self.symbols} on {self.df.index[i]}')
                # return self.symbols , self.df.index[i]
            
            if(float(close[curr_candle]) < float(close[previous_candle]) and \
                float(close[previous_candle]) < float(close[two_candles]) and \
                    float(open[previous_candle]) <= half_body_candle_3 and\
                float(close[previous_candle])<= half_body_candle_1 and \
                    bottom_shadow_1 < (50 * self.pip_size) and bottom_shadow_2 < (50 * self.pip_size) and \
                        bottom_shadow_3 < (50 * self.pip_size) ):
                print(f'three black crows found at {self.symbols} on {self.df.index[i]}')
                
        return self.symbols, self.df.index[i] 

    