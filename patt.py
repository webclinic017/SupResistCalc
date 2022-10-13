"""
A simple function call placing all the listed patterns in one place to make for an easier and neater code.

"""

import Patterns as PatRecog

def adding_all_patterns(df,symbol,end_date,start_date, pips):
    patrecog = PatRecog.PatternRecognition(df[symbol],symbol, end_date, start_date, pips)
    doj = patrecog.doji()
    print(f'doji = {doj}')
    engulfing = patrecog.engulf()
    print(f'Engulfing patt = {engulfing}')
    hammer = patrecog.hammer()
    print(f'hammer = {hammer}')
    three_sold = patrecog.three_soldiers()
    print(f'three soldiers = {three_sold}')
