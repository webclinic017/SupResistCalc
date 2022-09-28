import config
import supresistlines as supres
import oandapyV20
import oandapyV20.endpoints.forexlabs as labs
import oandapyV20.endpoints.instruments as instruments
import requests
import pandas as pd

if __name__ == '__main__':

    # Detecting levels on the higher timeframe
    # lists to store the screened results
    screened_list_1 = [] 
    screened_list_2 = []
    symbols = supres.symbol('all')
    h_gran = 'D'
    l_gran = 'H4'
    from_date = '2022-03-01'
    for sym in symbols:
        try:
            df = supres.get_data(symbols=sym,gran=h_gran,from_date= from_date)
            df[sym] = pd.DataFrame(df[sym], index = df[sym].index)

            levels_1 = supres.detect_level_method_1(df[sym])
            if (supres.has_breakout(levels_1[-5:],df[sym].iloc[-2], df[sym].iloc[-1])):
                supres.screened_list_1.append(sym)

            levels_2 = supres.detect_level_method_2(df[sym])
            if (supres.has_breakout(levels_2[-5:],df[sym].iloc[-2], df[sym].iloc[-1])):
                supres.screened_list_2.append(sym)
            
        except Exception as e:
            print(f'error - {e}')

    print(f'screened 1 = {supres.screened_list_1}')
    print(f'screened 2 = {supres.screened_list_2}')

    # Method 1: Using Fractal candlestick pattern (After the screener has run)
    for stock_code in supres.screened_list_1:
        df = supres.get_data(stock_code, gran=l_gran, from_date=from_date)
        lower_levels = []
        for i in range(2, len(df[stock_code])- 2):
            if supres.is_support(df[stock_code],i):
                l = float(df[stock_code]['Low'][i])
                if supres.is_far_from_level(l, lower_levels, df[stock_code]):
                    lower_levels.append((i,l))
                # df[stock_code].loc[df[stock_code].index[lower_levels[0]],'levels'] = [lower_levels[1]]
            elif supres.is_resistance(df[stock_code], i):
                l = float(df[stock_code]['High'][i])
                if supres.is_far_from_level(l, lower_levels, df[stock_code]):
                    lower_levels.append((i, l))
                # df[stock_code].loc[df[stock_code].index[lower_levels[0]],'levels'] = [lower_levels[1]]

        supres.plot_charts(symbols=stock_code, df=df[stock_code], gran=l_gran, levels=list(lower_levels))

    # Method 2: Window shifting method (After the screener has run)
    for symbols in supres.screened_list_2:
        df = supres.get_data(symbols, gran=l_gran, from_date=from_date)
        pivots = []
        max_list = []
        min_list = []
        for i in range(5, len(df[symbols])-5):
            high_range = df[symbols]['High'][i-5:i+4].astype(float)
            current_max = high_range.max()

            if current_max not in max_list:
                max_list = []
            max_list.append(current_max)

            if len(max_list) == 5 and supres.is_far_from_level(current_max,pivots, df[symbols]):
                pivots.append((i, current_max))

            low_range = df[symbols]['Low'][i-5:i+4].astype(float)
            current_min = low_range.min()
            if current_min not in min_list:
                min_list = []
            min_list.append(current_min)

            if len(min_list) == 5 and supres.is_far_from_level(current_min, pivots,df[symbols]):
                pivots.append((i, current_min))
        
        supres.plot_charts(symbols=symbols, df=df[symbols],gran=l_gran,levels=list(pivots))
