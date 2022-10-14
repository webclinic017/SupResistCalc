"""
A simple function call placing all the listed patterns in one place to make for an easier and neater code.

"""

import Candle_Patterns as PatRecog
import chart_patterns as ChartPat

def adding_all_candle_patterns(df,symbol,end_date,start_date, pips):
    patrecog = PatRecog.CandlePatternRecognition(df[symbol],symbol, end_date, start_date, pips)
    doj = patrecog.doji()
    engulfing = patrecog.engulf()
    hammer = patrecog.hammer()
    three_sold = patrecog.three_soldiers()
    tweezers = patrecog.tweezers()

    return doj, engulfing#, hammer ,three_sold, tweezers

def adding_all_chart_patterns(df,symbol,end,start,pips):
    chart_pat = ChartPat.ChartPatternRecognition(df[symbol],symbol,end,start,pips)
    flag = chart_pat.flag_pattern()
