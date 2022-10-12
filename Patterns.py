'''
This class attempts to define all the listed pattern groups and group them with either a 
(1) for buy or (-1) indicating its a sell

The patterns act as confluence when used in conjunction with support or resistance lines and help
provide the user with a direction with which to place trade.
'''

class PatternRecognition:
    def __init__(self,df,symbol, curr_date, start_date):
        self.df = df
        self.symbols = symbol
        self.curr_date = curr_date
        self.start_date = start_date
        self.df['Buy'] = " "
        self.df['Sell'] = " "

    def doji(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1

            if (float(open[curr_candle]) == float(close[curr_candle]) and float(open[previous_candle]) > float(close[previous_candle])):
                # self.df['Buy'][i] = 1
                print(f'bull doji spotted on {self.symbols} at {i} ')
                # np.where(open[i] == close[i], print(f'doji found on {self.symbols} at {i}'),nan)
                return self.symbols, self.df.index[i]

            if (float(open[curr_candle]) == float(close[curr_candle]) and float(close[previous_candle]) > float(open[previous_candle])):
                # self.df['Sell'][i] = -1
                print(f'bear doji found at {i} on {self.symbols}')
                return self.symbols, self.df.index[i]

        
    def bullengulf(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            # high= self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            two_candles = i-2
            body1 = round((float(close[curr_candle]) - (float(open[curr_candle]))),5)
            body2 = round((float(open[previous_candle]) - (float(close[previous_candle]))), 5)
            
            if (close[curr_candle] > open[curr_candle] and open[previous_candle] > close[previous_candle] and \
                open[two_candles] > close[two_candles] and close[previous_candle] < low[two_candles] and body1 > (2 * body2)):
                # self.df['Buy'][i] = 1
                print(f'bullengulf found at {i} on {self.symbols}')
                return self.symbols , self.df.index[i]

    def bearengulf(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            # low = self.df['Low']
            high = self.df['High']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            two_candles = i-2
            body1 = round((float(open[curr_candle]) - (float(close[curr_candle]))),5)
            body2 = round((float(close[previous_candle]) - (float(open[previous_candle]))), 5)


            if(open[curr_candle] > close[curr_candle] and close[previous_candle] > open[previous_candle] and \
                close[two_candles] > open[two_candles] and close[previous_candle] > high[two_candles] and body1 > (2 * body2)):
                # self.df['Sell'][i] = -1
                print(f'bearengulf found at {i} on {self.symbols}')
                return self.symbols , self.df.index[i]

    def hammer(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            # two_candles = i-2
            # max_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            # low_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            top_shadow = float(high[curr_candle]) - float(close[curr_candle])
            bottom_shadow = float(close[curr_candle]) - float(low[curr_candle])
            body1 = round((float(close[curr_candle]) - (float(open[curr_candle]))),5)

            if(float(high[curr_candle]) == float(close[curr_candle]) and float(close[previous_candle]) > float(open[previous_candle]) and bottom_shadow >= (2 * body1)):
                # self.df['Buy'][i] = 1
                print(f'hammer found  at {i} on {self.symbols}')
                return self.symbols , self.df.index[i]

            if(float(open[curr_candle]) == float(low[curr_candle]) and float(close[previous_candle]) > float(open[previous_candle]) and top_shadow >= (2 * body1)):
                # self.df['Buy'][i] = 1
                print(f'inv hammer found at {i} on {self.symbols}')
                return(self.symbols, self.df.index[i])

    def shooting_star(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i-1
            # two_candles = i-2
            # max_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            # low_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            top_shadow = float(high[curr_candle]) - float(close[curr_candle])
            bottom_shadow = float(close[curr_candle]) - float(low[curr_candle])
            body1 = round((float(close[curr_candle]) - (float(open[curr_candle]))),5)

            if(float(close[curr_candle]) == float(low[curr_candle]) and float(close[previous_candle]) > float(open[previous_candle]) and top_shadow >= (2 * body1)):
                # self.df['Sell'][i] = -1
                print(f'shooting star found at {i} on {self.symbols}')
                return self.symbols , self.df.index[i]

            if(float(open[curr_candle]) == float(high[curr_candle]) and float(close[previous_candle]) > float(open[previous_candle]) and bottom_shadow >= (2 * body1)):
                # self.df['Sell'][i] = -1
                print(f'hanging man found at {i} on {self.symbols}')
                return self.symbols , self.df.index[i]

    def three_white_soldiers(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i -1
            two_candles = i -2
            # max_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            # low_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            half_body_candle_2 = ((float(open[previous_candle]) - float(close[previous_candle]))/2) + float(close[previous_candle])
            half_body_candle_3 = ((float(open[two_candles]) - float(close[two_candles]))/2) + float(close[two_candles])


            if (float(open[curr_candle]) > float(open[previous_candle]) and float(open[previous_candle]) > float(open[two_candles]) and float(open[two_candles]) >= half_body_candle_3 and\
                float(open[curr_candle]) >= half_body_candle_2):
                print(f'three white soldiers found at {i} on {self.symbols}')
                return self.symbols , self.df.index[i]

    def three_black_crows(self):
        for i in range(len(self.df)-1):
            open = self.df['Open']
            high = self.df['High']
            low = self.df['Low']
            close = self.df['Close']
            curr_candle = i
            previous_candle = i -1
            two_candles = i -2
            # max_bar = max(float(open[curr_candle]), float(close[curr_candle]))
            # low_bar = min(float(open[curr_candle]), float(close[curr_candle]))
            half_body_candle_2 = ((float(open[previous_candle]) - float(close[previous_candle]))/2) + float(close[previous_candle])
            half_body_candle_3 = ((float(open[two_candles]) - float(close[two_candles]))/2) + float(close[two_candles])

            if(float(close[curr_candle]) < float(close[previous_candle]) and float(close[previous_candle]) < float(close[two_candles]) and float(close[two_candles]) <= half_body_candle_3 and\
                float(close[curr_candle])<= half_body_candle_2):
                print(f'three black crows found at {i} on {self.symbols}')
                return self.symbols, self.df.index[i] 