from cmath import nan
import pandas as pd
import numpy as np

class ChartPatternRecognition:
    def __init__(self,df,symbol, curr_date, start_date, pips):
        self.df = df
        self.symbols = symbol
        self.curr_date = curr_date
        self.start_date = start_date
        self.df['Buy'] = " "
        self.df['Sell'] = " "
        self.pip_size = pips

    def flag_pattern(self):
        date = self.df.index
        for i in range(len(self.df)):
            #movingMax returns the maximum price over the last t=20 timeperiods
            highest_close_of_flag = self.df['Close'].rolling(20).max()
            lowest_close_of_flag  = self.df['Close'].rolling(20).min()

            #movingMin returns the minimum price over the last t=20 timeperiods
            highest_close_of_poll = self.df['Close'].rolling(30).max()
            lowest_close_of_poll = self.df['Close'].rolling(30).min()            

            print(f'bull flag found at {self.symbols} on {date[i]}')

        return #bull_flag_trigger