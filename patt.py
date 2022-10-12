"""
A simple function call placing all the listed patterns in one place to make for an easier and neater code.

"""

import Patterns as PatRecog

def adding_all_patterns(df,symbol,end_date,start_date):
    patrecog = PatRecog.PatternRecognition(df[symbol],symbol, end_date, start_date)                    
    doj = patrecog.doji()
    print(f'doji = {doj}')
    bullengulfing = patrecog.bullengulf()
    print(f'bull = {bullengulfing}')
    bearengulfing = patrecog.bearengulf()
    print(f'bear = {bearengulfing}')
    hammer = patrecog.hammer()
    print(f'hammer = {hammer}')
    star = patrecog.shooting_star()
    print(f'star = {star}')
    three_white_sold = patrecog.three_white_soldiers()
    print(f'3 white sold = {three_white_sold}')
    three_black_crows = patrecog.three_black_crows()
    print(f'3 black crows = {three_black_crows}')
