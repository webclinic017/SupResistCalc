"""
A simple function call placing all the listed patterns in one place to make for an easier and neater code.

"""

import Patterns as PatRecog

def adding_all_patterns(df,symbol,end_date,start_date, pips):
    patrecog = PatRecog.PatternRecognition(df[symbol],symbol, end_date, start_date, pips)
    doj = patrecog.doji()
    engulfing = patrecog.engulf()
    hammer = patrecog.hammer()
    three_sold = patrecog.three_soldiers()

    return doj, engulfing, hammer ,three_sold