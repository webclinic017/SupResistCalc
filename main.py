import config
import supresistlines as supres
import oandapyV20
import oandapyV20.endpoints.forexlabs as labs
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

if __name__ == '__main__':

    # Detecting levels on the higher timeframe
    # lists to store the screened results
    screened_list_1 = [] 
    screened_list_2 = []
    levels = [] 
    pivots = [] 
    max_list = []
    min_list = []

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
                screened_list_1.append(sym)
            for sym in screened_list_1:
                for i in range(2, len(df[sym])- 2):
                    if supres.is_support(df[sym],i):
                        l = float(df[sym]['Low'][i])
                        if supres.is_far_from_level(l, levels, df[sym]):
                            levels.append((i,l))
                        # df[stock_code].loc[df[stock_code].index[lower_levels[0]],'levels'] = [lower_levels[1]]
                    elif supres.is_resistance(df[sym], i):
                        l = float(df[sym]['High'][i])
                        if supres.is_far_from_level(l, levels, df[sym]):
                            levels.append((i, l))
                        # df[stock_code].loc[df[stock_code].index[lower_levels[0]],'levels'] = [lower_levels[1]]

                supres.plot_charts(symbols=sym, df=df[sym], gran=h_gran, levels=list(levels_1))


            levels_2 = supres.detect_level_method_2(df[sym])
            if (supres.has_breakout(levels_2[-5:],df[sym].iloc[-2], df[sym].iloc[-1])):
                screened_list_2.append(sym)
            for sym in screened_list_2:
                for i in range(5, len(df[sym])-5):
                    high_range = df[sym]['High'][i-5:i+4].astype(float)
                    current_max = high_range.max()

                    if current_max not in max_list:
                        max_list = []
                    max_list.append(current_max)

                    if len(max_list) == 5 and supres.is_far_from_level(current_max,pivots, df[sym]):
                        pivots.append((i, current_max))

                    low_range = df[sym]['Low'][i-5:i+4].astype(float)
                    current_min = low_range.min()
                    if current_min not in min_list:
                        min_list = []
                    min_list.append(current_min)

                    if len(min_list) == 5 and supres.is_far_from_level(current_min, pivots,df[sym]):
                        pivots.append((i, current_min))
                
                supres.plot_charts(symbols=sym, df=df[sym],gran=h_gran,levels=list(levels_2))

        except Exception as e:
            print(f'error - {e}')

    print(f'screened 1 = {screened_list_1}')
    print(f'screened 2 = {screened_list_2}')

