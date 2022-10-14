import pandas as pd

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

            #We want poll to be much longer than the flag is wide.
            flag_width = highest_close_of_flag - lowest_close_of_flag
            poll_height = highest_close_of_poll - lowest_close_of_poll

            # ((new-old)/old) yields percentage gain between.
            bull_flag = (poll_height - flag_width ) / flag_width

            #Filter out bull flags who's flagpole tops go too high over the flapping flag
            bull_flag -= (highest_close_of_poll -highest_close_of_flag ) # highest_close_of_flag;

            thresh = 0.9
            bull_flag_trigger = (bull_flag > thresh)

            print(f'bull flag found at {self.symbols} on {date[i]}')
        return bull_flag_trigger